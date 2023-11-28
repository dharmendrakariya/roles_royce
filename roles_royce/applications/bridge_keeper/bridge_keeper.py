from web3 import Web3
from roles_royce.toolshed.alerting import SlackMessenger, TelegramMessenger, Messenger, LoggingLevel, \
    web3_connection_check
from roles_royce.toolshed.alerting.utils import get_tx_receipt_message_with_transfers
from prometheus_client import start_http_server as prometheus_start_http_server
import logging
from utils import ENV, SchedulerThread, Gauges, refill_bridge, invest_DAI, pay_interest, decimals_DAI, Flags, \
    log_initial_data, log_status_update
import time
import sys
import datetime
import schedule
from defabipedia.xDAI_bridge import ContractSpecs
from defabipedia.tokens import EthereumContractSpecs as Tokens
from defabipedia.types import Chains
from decimal import Decimal

# Importing the environment variables from the .env file
ENV = ENV()

# -----------------------------------------------------------------------------------------------------------------------

test_mode = ENV.TEST_MODE
if test_mode:
    from tests.utils import top_up_address

    w3_eth = Web3(Web3.HTTPProvider(f'http://localhost:{ENV.LOCAL_FORK_PORT_ETHEREUM}'))
    top_up_address(w3_eth, ENV.BOT_ADDRESS, 1)
    w3_gnosis = Web3(Web3.HTTPProvider(f'http://localhost:{ENV.LOCAL_FORK_PORT_GNOSIS}'))
    top_up_address(w3_gnosis, ENV.BOT_ADDRESS, 1)

# -----------------------------------------------------------------------------------------------------------------------

# Alert flags
flags = Flags()

# Messenger system
slack_messenger = SlackMessenger(webhook=ENV.SLACK_WEBHOOK_URL)
slack_messenger.start()
telegram_messenger = TelegramMessenger(bot_token=ENV.TELEGRAM_BOT_TOKEN, chat_id=ENV.TELEGRAM_CHAT_ID)
telegram_messenger.start()

# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger instance
logger = logging.getLogger(__name__)
messenger = Messenger(slack_messenger, telegram_messenger)

# Prometheus metrics from prometheus_client import Info
prometheus_start_http_server(ENV.PROMETHEUS_PORT)
gauges = Gauges()

# Exception and RPC endpoint failure counters
exception_counter = 0
rpc_endpoint_failure_counter = 0

# -----------------------------------------------------------------------------------------------------------------------

log_initial_data(ENV, messenger)

# -----------------------------------------------------------------------------------------------------------------------


def bot_do(w3_eth, w3_gnosis):
    global gauges
    global flags

    bot_ETH_balance = w3_eth.eth.get_balance(ENV.BOT_ADDRESS)

    if bot_ETH_balance < ENV.GAS_ETH_THRESHOLD * (10 ** 18):
        title = 'Lack of ETH for gas'
        message = f'  Im running outta ETH for gas! Only {bot_ETH_balance / (10 ** 18):,5f}%.5f ETH left.'
        messenger.log_and_alert(LoggingLevel.Warning, title, message, alert_flag=flags.lack_of_gas_warning.is_set())
        flags.lack_of_gas_warning.set()

    if bot_ETH_balance >= ENV.GAS_ETH_THRESHOLD and flags.lack_of_gas_warning.is_set():
        flags.lack_of_gas_warning.clear()

    DAI_contract = Tokens.DAI.contract(w3_eth)
    bridge_DAI_balance = DAI_contract.functions.balanceOf('0x4aa42145Aa6Ebf72e164C9bBC74fbD3788045016').call()

    interest_receiver_contract = ContractSpecs[Chains.Gnosis].BridgeInterestReceiver.contract(w3_gnosis)
    next_claim_epoch = interest_receiver_contract.functions.nextClaimEpoch().call()

    log_status_update(ENV, bridge_DAI_balance, bot_ETH_balance, next_claim_epoch)
    gauges.update(bridge_DAI_balance, bot_ETH_balance, next_claim_epoch)

    if bridge_DAI_balance < ENV.REFILL_THRESHOLD * (10 ** decimals_DAI):
        title = 'Refilling the bridge...'
        message = f'  The bridge"s DAI balance {bridge_DAI_balance / (10 ** decimals_DAI):.2f} dropped below the refill threshold {ENV.REFILL_THRESHOLD * (10 ** 18)}.'
        messenger.log_and_alert(LoggingLevel.Info, title, message)
        tx_receipt = refill_bridge(w3_eth, ENV)

        message, message_slack = get_tx_receipt_message_with_transfers(tx_receipt, ContractSpecs[
            Chains.Ethereum].xDaiBridge.address, w3_eth)
        messenger.log_and_alert(LoggingLevel.Info, f'Bridge refilled', message,
                                slack_msg=message_slack)

    elif bridge_DAI_balance > ENV.INVEST_THRESHOLD * (10 ** decimals_DAI):
        title = 'Investing DAI...'
        message = f'  The bridge"s DAI balance {bridge_DAI_balance / (10 ** decimals_DAI):.2f} surpassed the invest threshold {ENV.INVEST_THRESHOLD * (10 ** 18)}.'
        messenger.log_and_alert(LoggingLevel.Info, title, message)
        tx_receipt = invest_DAI(w3_eth, ENV)
        message, message_slack = get_tx_receipt_message_with_transfers(tx_receipt, ContractSpecs[
            Chains.Ethereum].xDaiBridge.address, w3_eth)
        messenger.log_and_alert(LoggingLevel.Info, f'DAI invested', message,
                                slack_msg=message_slack)

    if next_claim_epoch - 60 * ENV.MINUTES_BEFORE_CLAIM_EPOCH < time.time() < next_claim_epoch and not flags.interest_payed.is_set():
        title = 'Paying interest to interest receiver contract on Gnosis Chain...'
        tx_receipt = pay_interest(w3_eth, ENV, int(Decimal(ENV.AMOUNT_OF_INTEREST_TO_PAY) * Decimal(10 ** decimals_DAI)))
        message, message_slack = get_tx_receipt_message_with_transfers(tx_receipt, ContractSpecs[
            Chains.Ethereum].xDaiBridge.address, w3_eth)
        messenger.log_and_alert(LoggingLevel.Info, f'Interest payed', message,
                                slack_msg=message_slack)
        flags.interest_payed.set()
    elif time.time() > next_claim_epoch:
        flags.interest_payed.clear()

    log_status_update(ENV, bridge_DAI_balance, bot_ETH_balance, next_claim_epoch)
    gauges.update(bridge_DAI_balance, bot_ETH_balance, next_claim_epoch)


# -----------------------------MAIN LOOP-----------------------------------------

# Status notification scheduling
if ENV.STATUS_NOTIFICATION_HOUR != '':
    # FIXME: make sure the scheduling job is set at UTC time
    status_run_time = datetime.time(hour=ENV.STATUS_NOTIFICATION_HOUR, minute=0, second=0)
    schedule.every().day.at(str(status_run_time)).do(lambda: send_status_flag.set())
    scheduler_thread = SchedulerThread()
    scheduler_thread.start()

while True:

    try:
        if not test_mode:
            w3_eth, connection_check_eth = web3_connection_check(ENV.RPC_ENDPOINT_ETHEREUM, messenger,
                                                                 rpc_endpoint_failure_counter,
                                                                 ENV.RPC_ENDPOINT_ETHEREUM_FALLBACK)
            w3_gnosis, connection_check_gnosis = web3_connection_check(ENV.RPC_ENDPOINT_GNOSIS, messenger,
                                                                       rpc_endpoint_failure_counter,
                                                                       ENV.RPC_ENDPOINT_GNOSIS_FALLBACK)
            if not connection_check_eth or not connection_check_gnosis:
                continue
        else:
            w3_eth = Web3(Web3.HTTPProvider(f'http://localhost:{ENV.LOCAL_FORK_PORT_ETHEREUM}'))
            w3_gnosis = Web3(Web3.HTTPProvider(f'http://localhost:{ENV.LOCAL_FORK_PORT_GNOSIS}'))

        bot_do(w3_eth, w3_gnosis)

    except Exception as e:
        messenger.log_and_alert(LoggingLevel.Error, title='Exception', message='  ' + str(e.args[0]))
        exception_counter += 1
        if exception_counter == 5:  # TODO: this can be added as an environment variable
            messenger.log_and_alert(LoggingLevel.Error, title='Too many exceptions, exiting...', message='')
            time.sleep(5)  # Cooldown time for the messenger system to send messages in queue
            sys.exit(1)
    time.sleep(ENV.COOLDOWN_MINUTES * 60)
