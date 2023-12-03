from web3 import Web3
from roles_royce import roles
import roles_royce.protocols.eth.cowswap_signer as cowswap_signer
from roles_royce.constants import GCAddr
from tests.utils import (local_node_eth, accounts, fork_unlock_account, create_simple_safe, steal_token, top_up_address)
from tests.roles import setup_common_roles, deploy_roles, apply_presets
from defabipedia.types import Chains
from time import time
import pytest
from unittest import mock

def test_cowswap_signer_v1():
   mock_response = mock.Mock()
   mock_response.json.return_value = {
       'quote': {
           'buyAmount': 1000,
           'feeAmount': 100
       }
   }

   # Mock the requests.post function
   with mock.patch('requests.post', return_value=mock_response) as mock_post:
       # Now you can call the function you want to test
     
    avatar_safe = "0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f"

    sell_token = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    buy_token = "0x6810e776880C02933D47DB1b9fc05908e5386b96"
    sell_amount = 999749122606373987000
    kind = "sell"
    valid_to = int(30*60)
    valid_duration = 1700372412
    fee_amount_bp = 250877393626013  

    signer_tx = cowswap_signer.SignOrder(blockchain=Chains.Ethereum,
                                         avatar=avatar_safe,
                                         sell_token=sell_token,
                                         buy_token=buy_token,
                                         sell_amount=sell_amount,
                                         valid_to=valid_to,
                                         kind=kind,
                                         valid_duration=valid_duration,
                                         fee_amount_bp=fee_amount_bp)
    
    assert signer_tx.data == "0x569d34890000000000000000000000006b175474e89094c44da98b954eedeac495271d0f0000000000000000000000006810e776880c02933d47db1b9fc05908e5386b96000000000000000000000000458cd345b4c05e8df39d0a07220feb4ec19f5e6f000000000000000000000000000000000000000000000036324e621cd55ee2b800000000000000000000000000000000000000000000000000000000000003e80000000000000000000000000000000000000000000000000000000000000708970eb15ab11f171c843c2d1fa326b7f8f6bf06ac7f84bb1affcc86511c783f120000000000000000000000000000000000000000000000000000000000000064f3b277728b3fee749481eb3e0b3b48980dbbab78658fc419025cb16eee34677500000000000000000000000000000000000000000000000000000000000000005a28e9363bb942b639270062aa6bb295f434bcdfc42c97267bf003f272060dc95a28e9363bb942b639270062aa6bb295f434bcdfc42c97267bf003f272060dc90000000000000000000000000000000000000000000000000000000065599fbc0000000000000000000000000000000000000000000000000000e42bf1ede39d"


def test_cowswap_signer(local_node_eth, accounts):
    w3 = local_node_eth.w3
    
    avatar_safe = create_simple_safe(w3=w3, owner=accounts[0])
    steal_token(w3, "0x6C76971f98945AE98dD7d4DFcA8711ebea946eA6", "0x4D8027E6e6e3E1Caa9AC23267D10Fb7d20f85A37", avatar_safe.address, 100)
    roles_contract = deploy_roles(avatar=avatar_safe.address, w3=w3)
    setup_common_roles(avatar_safe, roles_contract)
    presets = """{
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

    apply_presets(avatar_safe, roles_contract, json_data=presets,
                  replaces=[("E522f854b978650Dc838Ade0e39FbC1417A2FfB0", "23dA9AdE38E4477b23770DeD512fD37b12381FAB")])

    blockchain = Chains.get_blockchain_from_web3(w3)

    avatar_safe_address = avatar_safe.address
    disassembler_address = accounts[4].address
    private_key = accounts[4].key
    role = 4

    sell_token = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    buy_token = "0x6810e776880C02933D47DB1b9fc05908e5386b96"
    sell_amount = 999749122606373987000
    kind = "sell"
    valid_to = int(30*60)
    valid_duration = 1700372412
    fee_amount_bp = 250877393626013 

    signer_tx = cowswap_signer.SignOrder(blockchain=blockchain,
                                         avatar=avatar_safe_address,
                                         sell_token=sell_token,
                                         buy_token=buy_token,
                                         sell_amount=sell_amount,
                                         valid_to=valid_to,
                                         kind=kind,
                                         valid_duration=valid_duration,
                                         fee_amount_bp=fee_amount_bp)
    
    
    checking = roles.send([signer_tx], 
                           role=role, 
                           private_key=private_key,
                           roles_mod_address=roles_contract.address,
                           web3=w3)
    
    assert checking