from ..types import Chain, ContractSpec, current_dir


class EthereumContractSpecs:
    xDaiBridge = ContractSpec(
        address="0x4aa42145Aa6Ebf72e164C9bBC74fbD3788045016",
        abi_path=current_dir() / "xdai_bridge.json",
        name="xdai_bridge",
    )


class GnosisContractSpecs:
    BridgeInterestReceiver = ContractSpec(
        address="0x670daeaF0F1a5e336090504C68179670B5059088",
        abi_path=current_dir() / "bridge_interest_receiver.json",
        name="bridge_interest_receiver",
    )


ContractSpecs = {Chain.ETHEREUM: EthereumContractSpecs, Chain.GNOSIS: GnosisContractSpecs}
