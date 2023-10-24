from roles_royce.constants import Chains
from roles_royce.abi_utils import load_abi, ContractSpec, ContractAbi
from ..tokens import Abis as TokenAbis


class EthereumAbis(TokenAbis):  # The inheritance with TokenAbis adds the ERC20 abi
    PriceOracle = ContractAbi(abi=load_abi('price_oracle.json'), name='price_oracle')
    LendingPool = ContractAbi(abi=load_abi('lending_pool.json'), name='lending_pool')


class EthereumContractSpecs:
    ProtocolDataProvider = ContractSpec(address='0xFc21d6d146E6086B8359705C8b28512a983db0cb',
                                        abi=load_abi('protocol_data_provider.json'),
                                        name='protocol_data_provider')
    PoolAddressesProvider = ContractSpec(address='0x02C3eA4e34C0cBd694D2adFa2c690EECbC1793eE',
                                         abi=load_abi('pool_addresses_provider.json'),
                                         name='pool_addresses_provider')


ContractSpecs = {
    Chains.Ethereum: EthereumContractSpecs
}

Abis = {
    Chains.Ethereum: EthereumAbis
}
