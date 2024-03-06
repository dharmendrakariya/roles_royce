from ..types import Chain, ContractSpec, current_dir


class EthereumContractSpecs:
    stETH = ContractSpec(
        address="0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84", abi_path=current_dir() / "steth.json", name="steth"
    )
    wstETH = ContractSpec(
        address="0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0", abi_path=current_dir() / "wsteth.json", name="wsteth"
    )


class GnosisContractSpecs:
    # TODO not available at this point in gc
    # stETH = ContractSpec(address='0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84',
    #                                     abi=load_abi('steth.json'),
    #                                     name='steth')
    wstETH = ContractSpec(
        address="0x6C76971f98945AE98dD7d4DFcA8711ebea946eA6", abi_path=current_dir() / "wsteth.json", name="wsteth"
    )


ContractSpecs = {Chain.ETHEREUM: EthereumContractSpecs, Chain.GNOSIS: GnosisContractSpecs}
