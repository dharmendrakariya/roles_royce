from web3.exceptions import TimeExhausted
from roles_royce.applications.panic_button_app.utils import ENV, ExecConfig
from tests.utils import assign_role, local_node_eth, accounts
import os
import json
import pytest
import subprocess
from pathlib import Path
import time

dao = 'GnosisDAO'
blockchain = 'ETHEREUM'
avatar_safe_address = '0x849D52316331967b6fF1198e5E32A0eB168D039d'
roles_mod_address = '0x1cFB0CD7B1111bf2054615C7C491a15C4A3303cc'
role = 4


def set_env(monkeypatch, private_key: str) -> ENV:
    monkeypatch.setenv('ETHEREUM_RPC_ENDPOINT', 'DummyString')
    monkeypatch.setenv('ETHEREUM_RPC_ENDPOINT_FALLBACK', 'DummyString')
    monkeypatch.setenv('GNOSISDAO_ETHEREUM_AVATAR_SAFE_ADDRESS', avatar_safe_address)
    monkeypatch.setenv('GNOSISDAO_ETHEREUM_ROLES_MOD_ADDRESS', roles_mod_address)
    monkeypatch.setenv('GNOSISDAO_ETHEREUM_ROLE', role)
    monkeypatch.setenv('GNOSISDAO_ETHEREUM_PRIVATE_KEY', private_key)
    # Without setting the MODE env it will default to DEVELOPMENT and use the local fork
    return ENV(dao, blockchain)


def set_up_roles(local_node_eth, accounts):
    block = 18421437
    local_node_eth.set_block(block)

    disassembler_address = accounts[0].address
    private_key = accounts[0].key.hex()

    assign_role(local_node=local_node_eth,
                avatar_safe_address=avatar_safe_address,
                roles_mod_address=roles_mod_address,
                role=role,
                asignee=disassembler_address)
    return private_key


JSON_FORM = {
    "protocol": "Aura",
    "exit_strategy": "exit_2_1",
    "percentage": 21,
    "exit_arguments": {

        "rewards_address": "0xDd1fE5AD401D4777cE89959b7fa587e569Bf125D",
        "max_slippage": 0.01
    }
}

exec_config = ExecConfig(percentage=JSON_FORM["percentage"],
                         dao=dao,
                         blockchain=blockchain,
                         protocol=JSON_FORM["protocol"],
                         exit_strategy=JSON_FORM["exit_strategy"],
                         exit_arguments=[JSON_FORM["exit_arguments"]])

transactions = [{'chainId': 1,
                 'data': '0x6928e74b000000000000000000000000dd1fe5ad401d4777ce89959b7fa587e569bf125d000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000044c32e7202000000000000000000000000000000000000000000000012c03e0fdb2d857add000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000',
                 'from': '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266',
                 'gas': 1043653,
                 'maxFeePerGas': 3710601020,
                 'maxPriorityFeePerGas': 2608114460,
                 'nonce': 558,
                 'to': '0x1cFB0CD7B1111bf2054615C7C491a15C4A3303cc',
                 'value': 0},
                {'chainId': 1,
                 'data': '0x6928e74b000000000000000000000000a238cbeb142c10ef7ad8442c6d1f9e89e07e7761000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000003648d80ff0a0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000031200dd1fe5ad401d4777ce89959b7fa587e569bf125d00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000044c32e7202000000000000000000000000000000000000000000000012c03e0fdb2d857add000000000000000000000000000000000000000000000000000000000000000100ba12222222228d8ba445958a75a0704d566bf2c8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002248bdb39131e19cf2d73a72ef1332c882f20534b6519be0276000200000000000000000112000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d0000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000014000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000ae78736cd615f374d3085123a210448e74fc6393000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000008c00cd28d990f445d0000000000000000000000000000000000000000000000098be067f12f90852400000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000012c03e0fdb2d857add000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
                 'from': '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266',
                 'gas': 1422520,
                 'maxFeePerGas': 1000000025,
                 'maxPriorityFeePerGas': 1000000016,
                 'nonce': 558,
                 'to': '0x1cFB0CD7B1111bf2054615C7C491a15C4A3303cc',
                 'value': 0},
                {'chainId': 1,
                 'data': '0x6928e74b000000000000000000000000a238cbeb142c10ef7ad8442c6d1f9e89e07e7761000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000003848d80ff0a0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000033200dd1fe5ad401d4777ce89959b7fa587e569bf125d00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000044c32e7202000000000000000000000000000000000000000000000012c03e0fdb2d857add000000000000000000000000000000000000000000000000000000000000000100ba12222222228d8ba445958a75a0704d566bf2c8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002448bdb39131e19cf2d73a72ef1332c882f20534b6519be0276000200000000000000000112000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d0000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000014000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000ae78736cd615f374d3085123a210448e74fc6393000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000001186347e057488a730000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000012c03e0fdb2d857add0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
                 'from': '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266',
                 'gas': 1440091,
                 'maxFeePerGas': 1000000025,
                 'maxPriorityFeePerGas': 1000000016,
                 'nonce': 558,
                 'to': '0x1cFB0CD7B1111bf2054615C7C491a15C4A3303cc',
                 'value': 0}
                ]


@pytest.mark.parametrize("tx", transactions)
def test_execute(local_node_eth, accounts, monkeypatch, tx):
    private_key = set_up_roles(local_node_eth, accounts)
    set_env(monkeypatch, private_key)

    file_path_execute = os.path.join(Path(os.path.dirname(__file__)).resolve().parent.parent.parent, 'roles_royce',
                                     'applications', 'panic_button_app',
                                     'execute.py')

    arguments = [
        'python', file_path_execute,
        '--dao', dao,
        '--blockchain', blockchain,
        '--transaction', json.dumps(tx)
    ]

    main = subprocess.run(arguments, capture_output=True, text=True)

    assert main.returncode == 0
    dict_message_stdout = json.loads(main.stdout[:-1])
    assert dict_message_stdout['status'] == 200
    # #  If we don't wait for the transaction to be validated, the next test will fail when trying to reset Anvil
    # time.sleep(5)
    # w3 = local_node_eth.w3
    # try:
    #     w3.eth.wait_for_transaction_receipt(dict_message_stdout['tx_hash'], timeout=40, poll_latency=5)
    # except TimeExhausted:
    #     pass