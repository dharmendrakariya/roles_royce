from ..types import Chain, ContractAbi, ContractSpec, current_dir


class Abis:
    PriceOracle = ContractAbi(abi_path=current_dir() / "price_oracle.json", name="price_oracle")
    LendingPool = ContractAbi(abi_path=current_dir() / "lending_pool.json", name="lending_pool")


class EthereumContractSpecs:
    ProtocolDataProvider = ContractSpec(
        address="0xFc21d6d146E6086B8359705C8b28512a983db0cb",
        abi_path=current_dir() / "protocol_data_provider.json",
        name="protocol_data_provider",
    )
    PoolAddressesProvider = ContractSpec(
        address="0x02C3eA4e34C0cBd694D2adFa2c690EECbC1793eE",
        abi_path=current_dir() / "pool_addresses_provider.json",
        name="pool_addresses_provider",
    )
    LendingPoolV3 = ContractSpec(
        address="0xC13e21B648A5Ee794902342038FF3aDAB66BE987",
        abi_path=current_dir() / "lending_pool.json",
        name="LendingPoolV3",
    )


class GnosisContractSpecs:
    ProtocolDataProvider = ContractSpec(
        address="0x2a002054A06546bB5a264D57A81347e23Af91D18",
        abi_path=current_dir() / "protocol_data_provider.json",
        name="protocol_data_provider",
    )
    PoolAddressesProvider = ContractSpec(
        address="0xA98DaCB3fC964A6A0d2ce3B77294241585EAbA6d",
        abi_path=current_dir() / "pool_addresses_provider.json",
        name="pool_addresses_provider",
    )


ContractSpecs = {Chain.ETHEREUM: EthereumContractSpecs, Chain.GNOSIS: GnosisContractSpecs}

Abis = {Chain.ETHEREUM: Abis, Chain.GNOSIS: Abis}
