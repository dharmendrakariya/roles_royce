from roles_royce.constants import ETHAddr
from tests.utils import (local_node_eth, accounts, fork_unlock_account, create_simple_safe, steal_token, top_up_address)
from roles_royce.toolshed.disassembling import LidoDisassembler
from defabipedia.types import Chains, ContractSpec
from decimal import Decimal
from roles_royce.evm_utils import erc20_abi
from tests.roles import setup_common_roles, deploy_roles, apply_presets
from pytest import approx
from roles_royce.roles_modifier import set_gas_strategy, GasStrategies
from defabipedia.lido import ContractSpecs
from roles_royce.protocols.eth import lido
import pytest
import json
import requests
from time import time

presets = """{
  "version": "1.0",
  "chainId": "1",
  "meta": {
    "name": null,
    "description": "",
    "txBuilderVersion": "1.8.0"
  },
  "createdAt": 1701637793776,
  "transactions": [
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x5e8266950000000000000000000000000000000000000000000000000000000000000004000000000000000000000000ae7ab96520de3a18e5e111b5eaab095312d7fe84",
      "value": "0"
    },
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x33a0480c0000000000000000000000000000000000000000000000000000000000000004000000000000000000000000ae7ab96520de3a18e5e111b5eaab095312d7fe84095ea7b300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
      "value": "0"
    },
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x939337720000000000000000000000000000000000000000000000000000000000000004000000000000000000000000ae7ab96520de3a18e5e111b5eaab095312d7fe84095ea7b3000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000200000000000000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000889edc2edab5f40e902b864ad4d7ade8e412f9b1",
      "value": "0"
    },
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x5e82669500000000000000000000000000000000000000000000000000000000000000040000000000000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca0",
      "value": "0"
    },
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x33a0480c00000000000000000000000000000000000000000000000000000000000000040000000000000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca0095ea7b30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000889edc2edab5f40e902b864ad4d7ade8e412f9b1",
      "value": "0"
    },
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x5e8266950000000000000000000000000000000000000000000000000000000000000004000000000000000000000000889edc2edab5f40e902b864ad4d7ade8e412f9b1",
      "value": "0"
    },
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x33a0480c0000000000000000000000000000000000000000000000000000000000000004000000000000000000000000889edc2edab5f40e902b864ad4d7ade8e412f9b1d6681042000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000220000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e1",
      "value": "0"
    },
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x33a0480c0000000000000000000000000000000000000000000000000000000000000004000000000000000000000000889edc2edab5f40e902b864ad4d7ade8e412f9b119aa6257000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000220000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e1",
      "value": "0"
    },
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x2fcf52d10000000000000000000000000000000000000000000000000000000000000004000000000000000000000000889edc2edab5f40e902b864ad4d7ade8e412f9b1e3afe0a3000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
      "value": "0"
    }
  ]
}"""



def test_integration_exit_1(local_node_eth, accounts):
    w3 = local_node_eth.w3
    block = 18421437
    local_node_eth.set_block(block)

    avatar_safe = create_simple_safe(w3=w3, owner=accounts[0])
    roles_contract = deploy_roles(avatar=avatar_safe.address, w3=w3)
    setup_common_roles(avatar_safe, roles_contract)
    apply_presets(avatar_safe, roles_contract, json_data=presets,
                  replaces=[("c01318bab7ee1f5ba734172bf7718b5dc6ec90e1", avatar_safe.address[2:])])
    
    blockchain = Chains.get_blockchain_from_web3(w3)
    steal_token(w3=w3, token=ContractSpecs[blockchain].stETH.address, holder="0xE53FFF67f9f384d20Ebea36F43b93DC49Ed22753",
                to=avatar_safe.address, amount=8_999_999_999_999_000_000)
    


    avatar_safe_address = avatar_safe.address
    disassembler_address = accounts[4].address
    private_key = accounts[4].key
    role = 4

    lido_disassembler = LidoDisassembler(w3=w3,
                                        avatar_safe_address=avatar_safe.address,
                                        roles_mod_address=roles_contract.address,
                                        role=role,
                                        signer_address=disassembler_address)
    
    steth_contract = ContractSpecs[blockchain].stETH.contract(w3)
    steth_balance = steth_contract.functions.balanceOf(avatar_safe_address).call()
    assert steth_balance == 8999999999998999998

    txn_transactable = lido_disassembler.exit_1(percentage=50)
    lido_disassembler.send(txn_transactable, private_key=private_key)
    nft_ids = lido.GetWithdrawalRequests(owner=avatar_safe_address).call(w3)
    assert len(nft_ids) == 1

    steth_balance = steth_contract.functions.balanceOf(avatar_safe_address).call()
    assert steth_balance == 4499999999999500000

def test_integration_exit_2(local_node_eth, accounts):
    w3 = local_node_eth.w3
    block = 18710862
    local_node_eth.set_block(block)
    
    avatar_safe = create_simple_safe(w3=w3, owner=accounts[0])
    roles_contract = deploy_roles(avatar=avatar_safe.address, w3=w3)
    setup_common_roles(avatar_safe, roles_contract)

    apply_presets(avatar_safe, roles_contract, json_data=presets,
                  replaces=[("c01318bab7ee1f5ba734172bf7718b5dc6ec90e1", avatar_safe.address[2:])])
    
    blockchain = Chains.get_blockchain_from_web3(w3)
    steal_token(w3=w3, token=ContractSpecs[blockchain].wstETH.address, holder="0x4dCbB1fE5983ad5b44DC661273a4f11CA812f8B8",
                to=avatar_safe.address, amount=8_999_999_999_999_000_000)
    

    avatar_safe_address = avatar_safe.address
    disassembler_address = accounts[4].address
    private_key = accounts[4].key
    role = 4

    lido_disassembler = LidoDisassembler(w3=w3,
                                        avatar_safe_address=avatar_safe.address,
                                        roles_mod_address=roles_contract.address,
                                        role=role,
                                        signer_address=disassembler_address)
    
    wsteth_contract = ContractSpecs[blockchain].wstETH.contract(w3)
    wsteth_balance = wsteth_contract.functions.balanceOf(avatar_safe_address).call()
    assert wsteth_balance == 8999999999999000000

    txn_transactable = lido_disassembler.exit_2(percentage=50)
    lido_disassembler.send(txn_transactable, private_key=private_key)
    nft_ids = lido.GetWithdrawalRequests(owner=avatar_safe_address).call(w3)
    assert len(nft_ids) == 1

    wsteth_balance = wsteth_contract.functions.balanceOf(avatar_safe_address).call()
    assert wsteth_balance == 4499999999999500000

preset_cowswap = """{
  "version": "1.0",
  "chainId": "1",
  "meta": {
    "name": null,
    "description": "",
    "txBuilderVersion": "1.8.0"
  },
  "createdAt": 1700857590822,
  "transactions": [
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x2933ef1c0000000000000000000000000000000000000000000000000000000000000004000000000000000000000000deb83d81d4a9758a7baec5749da863c409ea6c6b83afcefd00000000000000000000000000000000000000000000000000000000",
      "value": "0"
    },
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x5e826695000000000000000000000000000000000000000000000000000000000000000400000000000000000000000023da9ade38e4477b23770ded512fd37b12381fab",
      "value": "0"
    },
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x33a0480c000000000000000000000000000000000000000000000000000000000000000400000000000000000000000023da9ade38e4477b23770ded512fd37b12381fab569d3489000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000280000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e1",
      "value": "0"
    },
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x93933772000000000000000000000000000000000000000000000000000000000000000400000000000000000000000023da9ade38e4477b23770ded512fd37b12381fab569d3489000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000000000000000000000000000000000000000000d00000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000001e00000000000000000000000000000000000000000000000000000000000000220000000000000000000000000000000000000000000000000000000000000026000000000000000000000000000000000000000000000000000000000000002a000000000000000000000000000000000000000000000000000000000000002e00000000000000000000000000000000000000000000000000000000000000320000000000000000000000000000000000000000000000000000000000000036000000000000000000000000000000000000000000000000000000000000003a000000000000000000000000000000000000000000000000000000000000003e00000000000000000000000000000000000000000000000000000000000000420000000000000000000000000000000000000000000000000000000000000046000000000000000000000000000000000000000000000000000000000000004a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c0c293ce456ff0ed870add98a0828dd4d2903dbf0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000ba100000625a3754423978a60c9317c58a424e3d0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c00e94cb662c3520282e6f5717214004a7f268880000000000000000000000000000000000000000000000000000000000000020000000000000000000000000d533a949740bb3306d119cc777fa900ba034cd5200000000000000000000000000000000000000000000000000000000000000200000000000000000000000004e3fbd56cd56c3e72c1403e103b45db9da5b9d2b00000000000000000000000000000000000000000000000000000000000000200000000000000000000000006b175474e89094c44da98b954eedeac495271d0f00000000000000000000000000000000000000000000000000000000000000200000000000000000000000005a98fcbea516cf06857215779fd812ca3bef1b320000000000000000000000000000000000000000000000000000000000000020000000000000000000000000ae78736cd615f374d3085123a210448e74fc6393000000000000000000000000000000000000000000000000000000000000002000000000000000000000000048c3399719b582dd63eb5aadf12a40b4c3f52fa20000000000000000000000000000000000000000000000000000000000000020000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb480000000000000000000000000000000000000000000000000000000000000020000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec70000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000000200000000000000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca0",
      "value": "0"
    },
    {
      "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
      "data": "0x93933772000000000000000000000000000000000000000000000000000000000000000400000000000000000000000023da9ade38e4477b23770ded512fd37b12381fab569d3489000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000000000000000000000000000000000000000000700000000000000000000000000000000000000000000000000000000000000e00000000000000000000000000000000000000000000000000000000000000120000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000001e00000000000000000000000000000000000000000000000000000000000000220000000000000000000000000000000000000000000000000000000000000026000000000000000000000000000000000000000000000000000000000000000200000000000000000000000006b175474e89094c44da98b954eedeac495271d0f0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb480000000000000000000000000000000000000000000000000000000000000020000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec70000000000000000000000000000000000000000000000000000000000000020000000000000000000000000ae78736cd615f374d3085123a210448e74fc63930000000000000000000000000000000000000000000000000000000000000020000000000000000000000000ae7ab96520de3a18e5e111b5eaab095312d7fe840000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000000200000000000000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca0",
      "value": "0"
    }
  ]
}"""

preset_cowswap_easy ="""{
            "version": "1.0",
            "chainId": "1",
            "meta": {
                "description": "",
                "txBuilderVersion": "1.8.0"
            },
            "createdAt": 1700857590822,
            "transactions": [
                {
                "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
                "data": "0x5e8266950000000000000000000000000000000000000000000000000000000000000004000000000000000000000000E522f854b978650Dc838Ade0e39FbC1417A2FfB0",
                "value": "0"
                },
                {
                "to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86",
                "data": "0x2fcf52d10000000000000000000000000000000000000000000000000000000000000004000000000000000000000000E522f854b978650Dc838Ade0e39FbC1417A2FfB0569d3489000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002",
                "value": "0"
                }
            ]
            }"""


def test_integration_exit_3(local_node_eth, accounts):
    w3 = local_node_eth.w3

    block = 18421437
    #block = 18630000
    #block = 18800000
    #block = 18900000
    #block = 19000000
    #block = 19115000
    local_node_eth.set_block(block)
    avatar_safe = create_simple_safe(w3=w3, owner=accounts[0])
    roles_contract = deploy_roles(avatar=avatar_safe.address, w3=w3)
    setup_common_roles(avatar_safe, roles_contract)
    apply_presets(avatar_safe, roles_contract, json_data=preset_cowswap_easy,
                  replaces=[("E522f854b978650Dc838Ade0e39FbC1417A2FfB0", "23dA9AdE38E4477b23770DeD512fD37b12381FAB")])

    blockchain = Chains.get_blockchain_from_web3(w3)
    steal_token(w3=w3, token=ContractSpecs[blockchain].stETH.address, holder="0xE53FFF67f9f384d20Ebea36F43b93DC49Ed22753",
                to=avatar_safe.address, amount=8_999_999_999_999_000_000)
    
    avatar_safe_address = avatar_safe.address
    disassembler_address = accounts[4].address
    private_key = accounts[4].key
    role = 4

    lido_disassembler = LidoDisassembler(w3=w3,
                                        avatar_safe_address=avatar_safe.address,
                                        roles_mod_address=roles_contract.address,
                                        role=role,
                                        signer_address=disassembler_address)

    txn_transactable = lido_disassembler.exit_3(percentage=50,exit_arguments=[{"max_slippage": 0.01}])
    send_it = lido_disassembler.send(txn_transactable, private_key=private_key)
    assert send_it


    cow_api_address = "https://api.cow.fi/mainnet/api/v1/orders"
    send_order_api = {"sellToken": txn_transactable[0].args_list[0][0],
                        "buyToken": txn_transactable[0].args_list[0][1],
                        "receiver": txn_transactable[0].args_list[0][2],
                        "sellAmount": str(txn_transactable[0].args_list[0][3]),
                        "buyAmount": str(txn_transactable[0].args_list[0][4]),
                        "validTo": txn_transactable[0].args_list[0][5],
                        "feeAmount": str(txn_transactable[0].args_list[0][7]),
                        "kind": "sell",
                        "partiallyFillable": False,
                        "sellTokenBalance": "erc20",
                        "buyTokenBalance": "erc20",
                        "signingScheme": "presign",
                        "signature": "0x",
                        "from": txn_transactable[0].args_list[0][2],
                        "appData": json.dumps({"appCode":"santi_the_best"}),
                        "appDataHash": "0x970eb15ab11f171c843c2d1fa326b7f8f6bf06ac7f84bb1affcc86511c783f12"
                        }
    
    send_order = requests.post(cow_api_address, json=send_order_api)
    assert send_order.status_code == 201

    
def test_integration_exit_4(local_node_eth, accounts):
    w3 = local_node_eth.w3

    block = 18421437
    local_node_eth.set_block(block)
    avatar_safe = create_simple_safe(w3=w3, owner=accounts[0])
    roles_contract = deploy_roles(avatar=avatar_safe.address, w3=w3)
    setup_common_roles(avatar_safe, roles_contract)
    apply_presets(avatar_safe, roles_contract, json_data=preset_cowswap_easy,
                  replaces=[("E522f854b978650Dc838Ade0e39FbC1417A2FfB0", "23dA9AdE38E4477b23770DeD512fD37b12381FAB")])

    blockchain = Chains.get_blockchain_from_web3(w3)
    steal_token(w3=w3, token=ContractSpecs[blockchain].wstETH.address, holder="0xB0850a7589C195A6545Ed8A6a932B25B47003f2A",
                to=avatar_safe.address, amount=8_999_999_999_999_000_000)
    
    wsteth_contract = ContractSpecs[blockchain].wstETH.contract(w3)
    wsteth_balance = wsteth_contract.functions.balanceOf(avatar_safe.address).call()
    assert wsteth_balance == 8999999999999000000

    avatar_safe_address = avatar_safe.address
    disassembler_address = accounts[4].address
    private_key = accounts[4].key
    role = 4

    lido_disassembler = LidoDisassembler(w3=w3,
                                        avatar_safe_address=avatar_safe.address,
                                        roles_mod_address=roles_contract.address,
                                        role=role,
                                        signer_address=disassembler_address)

    txn_transactable = lido_disassembler.exit_4(percentage=50,exit_arguments=[{"max_slippage": 0.01}])
    send_it = lido_disassembler.send(txn_transactable, private_key=private_key)
    assert send_it

    cow_api_address = "https://api.cow.fi/mainnet/api/v1/orders"
    send_order_api = {"sellToken": txn_transactable[0].args_list[0][0],
                        "buyToken": txn_transactable[0].args_list[0][1],
                        "receiver": txn_transactable[0].args_list[0][2],
                        "sellAmount": str(txn_transactable[0].args_list[0][3]),
                        "buyAmount": str(txn_transactable[0].args_list[0][4]),
                        "validTo": txn_transactable[0].args_list[0][5],
                        "feeAmount": str(txn_transactable[0].args_list[0][7]),
                        "kind": "sell",
                        "partiallyFillable": False,
                        "sellTokenBalance": "erc20",
                        "buyTokenBalance": "erc20",
                        "signingScheme": "presign",
                        "signature": "0x",
                        "from": txn_transactable[0].args_list[0][2],
                        "appData": json.dumps({"appCode":"santi_the_best"}),
                        "appDataHash": "0x970eb15ab11f171c843c2d1fa326b7f8f6bf06ac7f84bb1affcc86511c783f12"
                        }
    
    send_order = requests.post(cow_api_address, json=send_order_api)
    assert send_order.status_code == 201










