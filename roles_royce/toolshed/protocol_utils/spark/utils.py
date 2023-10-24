from web3 import Web3
from roles_royce import addresses_and_abis
from dataclasses import dataclass
from enum import Enum
from roles_royce.constants import Chains


class SparkToken(Enum):
    """An Enum to handle Spark token types."""
    UNDERLYING = "underlying"
    INTEREST_BEARING = "interest_bearing"
    STABLE_DEBT = "stable_debt"
    VARIABLE_DEBT = "variable_debt"


@dataclass
class SparkUtils:
    """A class to handle miscellaneous tools for Spark protocol."""
    w3: Web3

    @staticmethod
    def get_chi(w3: Web3, block: int | str = 'latest') -> int:
        blockchain = Chains.get_blockchain_from_web3(w3)
        maker_pot_contract = addresses_and_abis.maker.ContractSpecs[blockchain].Pot.contract(w3)
        ts = w3.eth.get_block(block)['timestamp']
        rho = maker_pot_contract.functions.rho().call(block_identifier=block)
        if ts > rho:
            chi = maker_pot_contract.functions.drip().call(block_identifier=block)
        else:
            chi = maker_pot_contract.functions.chi().call(block_identifier=block)
        return chi

    @staticmethod
    def get_spark_token_addresses(w3: Web3, block: int | str = 'latest') -> list[dict]:
        blockchain = Chains.get_blockchain_from_web3(w3)
        protocol_data_provider_contract = addresses_and_abis.spark.ContractSpecs[blockchain].ProtocolDataProvider.contract(w3)
        reserve_tokens = protocol_data_provider_contract.functions.getAllReservesTokens().call(block_identifier=block)
        spark_tokens = []
        for token in reserve_tokens:
            data = protocol_data_provider_contract.functions.getReserveTokensAddresses(token[1]).call(
                block_identifier=block)
            spark_tokens.append(
                {SparkToken.UNDERLYING: token[1], SparkToken.INTEREST_BEARING: data[0],
                 SparkToken.STABLE_DEBT: data[1], SparkToken.VARIABLE_DEBT: data[2]}
            )
        return spark_tokens
