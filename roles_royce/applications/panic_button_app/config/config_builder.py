import json
from web3.types import Address
from web3 import Web3
from roles_royce.constants import StrEnum
from .utils import get_tokens_from_bpt, get_gauge_address_from_bpt, get_aura_gauge_from_bpt
import os
from dataclasses import dataclass
from defabipedia.types import Blockchain, Chains
import copy
from defabipedia.lido import ContractSpecs


# -----------------------------------------------------------------------------------------------------------------------
# StrEnums
# -----------------------------------------------------------------------------------------------------------------------

class DAO(StrEnum):
    GnosisDAO = "GnosisDAO"
    GnosisLTD = "GnosisLTD"

    def __str__(self):
        return self.name


class Protocol(StrEnum):
    Balancer = "Balancer"
    Aura = "Aura"
    Lido = "Lido"

    def __str__(self):
        return self.name


# -----------------------------------------------------------------------------------------------------------------------
# General
# -----------------------------------------------------------------------------------------------------------------------

def seed_file(dao: DAO, blockchain: Blockchain) -> None:
    file = os.path.join(os.path.dirname(__file__), 'strategies', f"{dao}-{blockchain}.json")
    with open(file, "w") as f:
        data = {
            "dao": dao,
            "blockchain": f'{blockchain}',
            "general_parameters": [
                {
                    "name": "percentage",
                    "label": "Percentage",
                    "type": "input",
                    "rules": {
                        "min": 0,
                        "max": 100
                    }
                }
            ],
            "positions": []
        }
        json.dump(data, f)


# -----------------------------------------------------------------------------------------------------------------------
# Position classes
# -----------------------------------------------------------------------------------------------------------------------

@dataclass
class BalancerPosition:
    position_id: str
    bpt_address: Address
    staked: bool

    def __post_init__(self):
        self.bpt_address = Web3.to_checksum_address(self.bpt_address)

    def position_id_tech(self, w3: Web3) -> Address:
        """Returns the address of the BPT if staked is False, otherwise the address of the BPT gauge token

        Args:
            w3: Web3 instance

        Returns:
            Address of the BPT is stake is False, or BPT gauge token if stake is True
        """
        if self.staked:
            gauge_address = get_gauge_address_from_bpt(w3, self.bpt_address)
            position_id_tech = gauge_address
        else:
            position_id_tech = self.bpt_address
        return position_id_tech

    def position_id_human_readable(self, w3: Web3, pool_tokens: list[dict] = None) -> str:
        """Returns a string with the name of the protocol and the symbols of the tokens in the pool, specifying if the
        BPT is staked in the gauge or not, e.g. Balancer_DAI_WETH_staked or Balancer_DAI_WETH.

        Args:
            w3: Web3 instance
            pool_tokens: List of dictionaries with the token address and symbol for each token in the pool

        Returns:
            String with the name of the protocol and the symbols of the tokens in the pool, adding _staked if the BPT
            is staked in the gauge.

        """
        if pool_tokens is None:
            pool_tokens = get_tokens_from_bpt(w3, self.bpt_address)
        result = f'{Chains.get_blockchain_from_web3(w3)}_Balancer'
        for token in pool_tokens:
            result= result + f"_{token['symbol']}"
        if self.staked:
            result = result + "_staked"
        return result


@dataclass
class AuraPosition:
    position_id: str
    bpt_address: Address

    def __post_init__(self):
        self.bpt_address = Web3.to_checksum_address(self.bpt_address)

    def position_id_tech(self, w3: Web3) -> Address:
        """Returns the address of the Aura gauge token"""
        return get_aura_gauge_from_bpt(w3, self.bpt_address)

    def position_id_human_readable(self, w3: Web3, pool_tokens: list[dict] = None) -> str:
        if pool_tokens is None:
            pool_tokens = get_tokens_from_bpt(w3, self.bpt_address)
        result = f'{Chains.get_blockchain_from_web3(w3)}_Aura'
        for token in pool_tokens:
            result = result + f"_{token['symbol']}"
        return result
    
@dataclass
class LidoPosition:
    position_id: str
    lido_address: Address

    def position_id_tech(self) -> Address:
        """Returns either stETH or wstETH address"""
        return self.lido_address
    
    def position_id_human_readable(self, w3: Web3) -> str:
        blockchain = Chains.get_blockchain_from_web3(w3)
        if self.lido_address == ContractSpecs[blockchain].stETH.address:
            return f'{blockchain}_Lido_stETH'
        else:
            return f'{blockchain}_Lido_wstETH'


# -----------------------------------------------------------------------------------------------------------------------
# Json builder
# -----------------------------------------------------------------------------------------------------------------------
@dataclass
class DAOStrategiesBuilder:
    dao: DAO
    blockchain: Blockchain
    balancer: list[BalancerPosition] | None = None
    aura: list[AuraPosition] | None = None
    lido: list[LidoPosition] | None = None

    def build_json(self, w3: Web3):
        print(f'Building json for {self.dao}-{self.blockchain}')
        print(f'    Adding Balancer positions')
        if self.balancer:
            self.add_to_json(self.build_balancer_positions(w3, self.balancer))
        print(f'    Adding Aura positions')
        if self.aura:
            self.add_to_json(self.build_aura_positions(w3, self.aura))
        print(f'    Adding Lido positions')
        if self.lido:
            self.add_to_json(self.build_lido_positions(self.lido))

    def add_to_json(self, positions: list[dict]):
        file = os.path.join(os.path.dirname(__file__), 'strategies', f"{self.dao}-{self.blockchain}.json")

        if not os.path.isfile(file):
            seed_file(self.dao, self.blockchain)

        with open(file, "r") as f:
            strategies = json.load(f)

        for position in positions:
            if position['position_id_tech'] in [position_element['position_id_tech'] for position_element in strategies["positions"]]:
                continue
            strategies['positions'].append(position)

        with open(file, "w") as f:
            json.dump(strategies, f, indent=4)

    @staticmethod
    def build_balancer_positions(w3: Web3, positions: list[BalancerPosition]) -> list[dict]: 
        with open(os.path.join(os.path.dirname(__file__), 'templates', 'balancer_template.json'), 'r') as f:
            balancer_template = json.load(f)
           
        result = []
        for balancer_position in positions:


            print("        Adding: ", balancer_position)

            bpt_address = balancer_position.bpt_address

            position = copy.deepcopy(balancer_template)

            if balancer_position.staked:
                for item in range(3):
                    position['exec_config'].pop(0)
                    gauge_address = balancer_position.position_id_tech(w3)
                for i in range(3):
                    position["exec_config"][i]["parameters"][0]["value"] = gauge_address
            else:
                for item in range(3):
                    position['exec_config'].pop(-1)
                for i in range(3):
                    position["exec_config"][i]["parameters"][0]["value"] = bpt_address

            del position["exec_config"][1]["parameters"][2]["options"][0]  # Remove the dummy element in template

            position["position_id"] = balancer_position.position_id

            try:
                pool_tokens = get_tokens_from_bpt(w3, bpt_address)
                position["position_id_tech"] = gauge_address if balancer_position.staked else bpt_address
                position["position_id_human_readable"] = balancer_position.position_id_human_readable(w3, pool_tokens=pool_tokens)
                for token in pool_tokens:
                    position["exec_config"][1]["parameters"][2]["options"].append({
                        "value": token['address'],
                        "label": token['symbol']
                    })

            except Exception as e:
                position["position_id_human_readable"] = f"AddressGivesError: {e}"

            result.append(position)

        return result

    @staticmethod
    def build_aura_positions(w3: Web3, positions: list[AuraPosition]) -> list[dict]:


        with open(os.path.join(os.path.dirname(__file__), 'templates', 'aura_template.json'), 'r') as f:
            aura_template = json.load(f)

        result = []
        for aura_position in positions:

            print("        Adding: ", aura_position)
            bpt_address = aura_position.bpt_address
            position = copy.deepcopy(aura_template)
            try:
                aura_address = aura_position.position_id_tech(w3)

                del position["exec_config"][2]["parameters"][2]["options"][0]  # Remove the dummy element in template

                position["position_id"] = aura_position.position_id
                position["position_id_tech"] = aura_address
                for i in range(4):
                    position["exec_config"][i]["parameters"][0]["value"] = aura_address
                pool_tokens = get_tokens_from_bpt(w3, bpt_address)
                position["position_id_human_readable"] = aura_position.position_id_human_readable(w3, pool_tokens=pool_tokens)
                for token in pool_tokens:
                    position["exec_config"][2]["parameters"][2]["options"].append({
                        "value": token['address'],
                        "label": token['symbol']
                    })

            except Exception as e:
                position["position_id_human_readable"] = f"AddressGivesError: {e}"

            result.append(position)

        return result

    @staticmethod
    def build_lido_positions(w3: Web3, positions: list[LidoPosition]) -> list[dict]:


        with open(os.path.join(os.path.dirname(__file__), 'templates', 'lido_template.json'), 'r') as f:
            lido_template = json.load(f)

        result = []
        for lido_position in positions:
            position["position_id"] = lido_position.position_id
            position["position_id_tech"] = lido_position.lido_address
            position["position_id_human_readable"] = lido_position.position_id_human_readable(w3)

            print("        Adding: ", lido_position)
            position = copy.deepcopy(lido_template)

            result.append(position)
        return result


