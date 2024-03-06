from ..types import Chain, ContractAbi, ContractSpec, current_dir


class AllAbis:
    BaseRewardPool = ContractAbi(abi_path=current_dir() / "base_reward_pool.json", name="base_reward_pool")


class EthereumContractSpecs:
    Booster = ContractSpec(
        address="0xA57b8d98dAE62B26Ec3bcC4a365338157060B234", abi_path=current_dir() / "booster.json", name="booster"
    )


class GnosisContractSpecs:
    Booster = ContractSpec(
        address="0x98Ef32edd24e2c92525E59afc4475C1242a30184", abi_path=current_dir() / "booster.json", name="booster"
    )


ContractSpecs = {Chain.ETHEREUM: EthereumContractSpecs, Chain.GNOSIS: GnosisContractSpecs}

Abis = {Chain.ETHEREUM: AllAbis, Chain.GNOSIS: AllAbis}
