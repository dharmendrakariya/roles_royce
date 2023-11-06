from roles_royce.protocols.eth import aave_v3
from .utils import (local_node_eth, accounts, get_balance, steal_token, create_simple_safe, top_up_address)
from .roles import setup_common_roles, deploy_roles, apply_presets
from roles_royce import roles
from roles_royce.constants import ETHAddr
from decimal import Decimal
from pytest import approx
from roles_royce.toolshed.protocol_utils.aave_v3.addresses_and_abis import AddressesAndAbis
from roles_royce.toolshed.protocol_utils.aave_v3.cdp import AaveV3CDPManager
from roles_royce.constants import Chain

USER = "0xDf3A7a27704196Af5149CD67D881279e32AF2C21"
AVATAR = "0x849D52316331967b6fF1198e5E32A0eB168D039d"

#-----------------------------------------------------#
"""Unit Tests"""
#-----------------------------------------------------#
def test_approve_token():
    method = aave_v3.ApproveToken(token=ETHAddr.WETH, amount=123)
    assert method.data == '0x095ea7b300000000000000000000000087870bca3f3fd6335c3f4ce8392d69350b4fa4e2000000000000000000000000000000000000000000000000000000000000007b'

def test_approve_AEthWETH():
    method = aave_v3.ApproveAEthWETH(amount=123)
    assert method.data == '0x095ea7b300000000000000000000000087870bca3f3fd6335c3f4ce8392d69350b4fa4e2000000000000000000000000000000000000000000000000000000000000007b'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].aEthWETH.address

def test_approve_stkAAVE():
    method = aave_v3.ApproveForStkAAVE(amount=123)
    assert method.data == '0x095ea7b30000000000000000000000004da27a545c0c5b758a6ba100e3a049001de870f5000000000000000000000000000000000000000000000000000000000000007b'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].AAVE.address

def test_approve_stkABPT():
    method = aave_v3.ApproveForStkABPT(amount=123)
    assert method.data == '0x095ea7b3000000000000000000000000a1116930326d21fb917d5a27f1e9943a9595fb47000000000000000000000000000000000000000000000000000000000000007b'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].ABPT.address

def test_approve_delegation():
    method = aave_v3.ApproveDelegation(target= AddressesAndAbis[Chain.Ethereum].variableDebtWETH.address, amount=123)
    assert method.data == '0xc04a8a10000000000000000000000000d322a49006fc828f9b5b37ab215f99b4e5cab19c000000000000000000000000000000000000000000000000000000000000007b'
    assert method.contract_address == '0xeA51d7853EEFb32b6ee06b1C12E6dcCA88Be0fFE'

def test_deposit_token():
    method = aave_v3.DepositToken(asset=ETHAddr.WETH, amount=123, avatar=AVATAR)
    assert method.data == '0x617ba037000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000000000000000000000000000000000000000007b000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d0000000000000000000000000000000000000000000000000000000000000000'

def test_withdraw_token():
    method = aave_v3.WithdrawToken(asset=ETHAddr.WETH, amount=123, avatar=AVATAR)
    assert method.data == '0x69328dec000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000000000000000000000000000000000000000007b000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d'

def test_deposit_ETH():
    method = aave_v3.DepositETH(eth_amount=123, avatar=AVATAR)
    assert method.data == '0x474cf53d00000000000000000000000087870bca3f3fd6335c3f4ce8392d69350b4fa4e2000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d0000000000000000000000000000000000000000000000000000000000000000'

def test_withdraw_ETH():
    method = aave_v3.WithdrawETH(amount=123, avatar=AVATAR)
    assert method.data == '0x80500d2000000000000000000000000087870bca3f3fd6335c3f4ce8392d69350b4fa4e2000000000000000000000000000000000000000000000000000000000000007b000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d'

def test_collateralize():
    method = aave_v3.Collateralize(asset=ETHAddr.WETH, use_as_collateral=True)
    assert method.data == '0x5a3b74b9000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000000000000000000000000000000000000000000001'

def test_borrow():
    method = aave_v3.Borrow(asset=ETHAddr.WETH, amount=123, interest_rate_mode=aave_v3.InterestRateMode.VARIABLE, avatar=AVATAR)
    assert method.data == '0xa415bcad000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000000000000000000000000000000000000000007b00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d'

def test_repay():
    method = aave_v3.Repay(asset=ETHAddr.WETH, amount=123, interest_rate_mode=aave_v3.InterestRateMode.VARIABLE, avatar=AVATAR)
    assert method.data == '0x573ade81000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000000000000000000000000000000000000000007b0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d'

def test_borrow_ETH():
    method = aave_v3.BorrowETH(amount=123, interest_rate_mode=aave_v3.InterestRateMode.VARIABLE)
    assert method.data == '0x66514c9700000000000000000000000087870bca3f3fd6335c3f4ce8392d69350b4fa4e2000000000000000000000000000000000000000000000000000000000000007b00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000'

def test_repay_ETH():
    method = aave_v3.RepayETH(eth_amount=123, interest_rate_mode=aave_v3.InterestRateMode.VARIABLE, avatar=AVATAR)
    assert method.data == '0x02c5fcf800000000000000000000000087870bca3f3fd6335c3f4ce8392d69350b4fa4e2000000000000000000000000000000000000000000000000000000000000007b0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d'

def test_swap_borrow_rate_mode():
    method = aave_v3.SwapBorrowRateMode(asset=ETHAddr.WETH, interest_rate_mode=aave_v3.InterestRateMode.VARIABLE)
    assert method.data == '0x94ba89a2000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000000000000000000000000000000000000000000002'

def test_stake_AAVE():
    method = aave_v3.StakeAAVE(avatar=AVATAR, amount=123)
    assert method.data == '0xadc9772e000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d000000000000000000000000000000000000000000000000000000000000007b'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].stkAAVE.address

def test_stake_ABPT():
    method = aave_v3.StakeABPT(avatar=AVATAR, amount=123)
    assert method.data == '0xadc9772e000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d000000000000000000000000000000000000000000000000000000000000007b'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].stkABPT.address

def test_claim_rewards_and_stake():
    method = aave_v3.ClaimRewardsAndStake(avatar=AVATAR, amount=123)
    assert method.data == '0x955e18af000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d000000000000000000000000000000000000000000000000000000000000007b'

def test_unstake_AAVE():
    method = aave_v3.UnstakeAAVE(avatar=AVATAR, amount=123)
    assert method.data == '0x1e9a6950000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d000000000000000000000000000000000000000000000000000000000000007b'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].stkAAVE.address

def test_unstake_ABPT():
    method = aave_v3.UnstakeABPT(avatar=AVATAR, amount=123)
    assert method.data == '0x1e9a6950000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d000000000000000000000000000000000000000000000000000000000000007b'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].stkABPT.address

def test_cooldown_stkAAVE():
    method = aave_v3.CooldownStkAAVE(value=123, avatar=AVATAR)
    assert method.data == '0x787a08a6'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].stkAAVE.address

def test_cooldown_stkABPT():
    method = aave_v3.CooldownStkABPT(value=123, avatar=AVATAR)
    assert method.data == '0x787a08a6'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].stkABPT.address

def test_claim_AAVE_rewards():
    method = aave_v3.ClaimAAVERewards(avatar=AVATAR, amount=123)
    assert method.data == '0x9a99b4f0000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d000000000000000000000000000000000000000000000000000000000000007b'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].stkAAVE.address

def test_claim_ABPT_rewards():
    method = aave_v3.ClaimABPTRewards(avatar=AVATAR, amount=123)
    assert method.data == '0x9a99b4f0000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d000000000000000000000000000000000000000000000000000000000000007b'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].stkABPT.address

def test_swap_and_repay():
    method = aave_v3.SwapAndRepay(collateral_asset=ETHAddr.USDC, 
                                  debt_asset=ETHAddr.WETH, 
                                  collateral_amount=123, 
                                  debt_repay_amount=123, 
                                  debt_rate_mode=aave_v3.InterestRateMode.VARIABLE, 
                                  buy_all_balance_offset=0, 
                                  calldata='0x0000000000000000000000000000000000000000000000000000000000000040000000000000000000000000def171fe48cf0115b1d80b88dc8eab59176fee5700000000000000000000000000000000000000000000000000000000000004842298207a00000000000000000000000000000000000000000000000000000000000000200000000000000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca0000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000000000562c9b4164b58103000000000000000000000000000000000000000000000000000000028fa6ae0000000000000000000000000000000000000000000000000056169161cebe049800000000000000000000000000000000000000000000000000000000000001e0000000000000000000000000000000000000000000000000000000000000022000000000000000000000000000000000000000000000000000000000000003a0000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009abf798f5314bfd793a9e57a654bed35af4a1d600100000000000000000000000000000000000000000000000000000000031388000000000000000000000000000000000000000000000000000000000000044000000000000000000000000000000000000000000000000000000000652742c577e189f1a03f43afae287d193069d849000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000e592427a0aece92de3edee1f18e0157c058615640000000000000000000000000000000000000000000000000000000000000144f28c0498000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000def171fe48cf0115b1d80b88dc8eab59176fee5700000000000000000000000000000000000000000000000000000000653028e4000000000000000000000000000000000000000000000000000000028fa6ae00000000000000000000000000000000000000000000000000562c9b4164b581010000000000000000000000000000000000000000000000000000000000000042a0b86991c6218b36c1d19d4a2e9eb0ce3606eb480001f4c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000647f39c581f595b53c5cb19bd0b3f8da6c935e2ca00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000014400000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 
                                  permit_amount=123, 
                                  permit_deadline=1697053784, 
                                  permit_v=27, 
                                  permit_r='0xf63fe2ddf43a364fb088ca5fbabc1928b6bbf11b35aec8502907902baf240935', 
                                  permit_s='0x3e452b86b67a5c5ce46fdc83c1e23db730f7e2b9aa1d12ab25faf581be38140b') 
    assert method.data == '0x9a99b4f0000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d000000000000000000000000000000000000000000000000000000000000007b'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].stkABPT.address

def test_delegate_AAVE():
    method = aave_v3.DelegateAAVE(delegatee=USER)
    assert method.data == '0x5c19a95c000000000000000000000000df3a7a27704196af5149cd67d881279e32af2c21'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].AAVE.address

def test_delegate_AAVE_by_type():
    method = aave_v3.DelegateAAVEByType(delegatee=USER, delegation_type=aave_v3.DelegationType.VOTING)
    assert method.data == '0xdc937e1c000000000000000000000000df3a7a27704196af5149cd67d881279e32af2c210000000000000000000000000000000000000000000000000000000000000000'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].AAVE.address

def test_delegate_stkAAVE():
    method = aave_v3.DelegateAAVE(delegatee=USER)
    assert method.data == '0x5c19a95c000000000000000000000000df3a7a27704196af5149cd67d881279e32af2c21'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].stkAAVE.address

def test_delegate_stkAAVE_by_type():
    method = aave_v3.DelegateAAVEByType(delegatee=USER, delegation_type=aave_v3.DelegationType.VOTING)
    assert method.data == '0xdc937e1c000000000000000000000000df3a7a27704196af5149cd67d881279e32af2c210000000000000000000000000000000000000000000000000000000000000000'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].stkAAVE.address

def test_submit_vote():
    method = aave_v3.SubmitVote(proposal_id=123, support=True)
    assert method.data == '0x612c56fa000000000000000000000000000000000000000000000000000000000000007b0000000000000000000000000000000000000000000000000000000000000001'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].GovernanceV2.address

def test_liquidation_call():
    method = aave_v3.LiquidationCall(collateral_asset=ETHAddr.WETH, debt_asset=ETHAddr.USDC, user=USER, debt_to_cover=123, receive_a_token=False)
    assert method.data == '0x612c56fa000000000000000000000000000000000000000000000000000000000000007b0000000000000000000000000000000000000000000000000000000000000001'
    assert method.contract_address == AddressesAndAbis[Chain.Ethereum].GovernanceV2.address

#-----------------------------------------------------#
"""Integration Tests"""
#-----------------------------------------------------#

def test_integration_liquidation_call(local_node_eth):
    w3 = local_node_eth.w3
    block = 18430238
    local_node_eth.set_block(block)

    cdp = AaveV3CDPManager(w3=w3, owner_address=USER)

    balances = cdp.get_cdp_balances_data(block=block)
    health_factor = cdp.get_health_factor(block=block)
    cdp_data = cdp.get_cdp_data(block=block)

    print(health_factor)