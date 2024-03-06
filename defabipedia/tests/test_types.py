from defabipedia.types import Chain


def test_equiality_with_str():
    assert Chain.ETHEREUM == "ethereum"
    assert Chain.ETHEREUM.name == "ethereum"
    assert Chain.ETHEREUM.chain_id == 1
    assert Chain.ETHEREUM == Chain.ETHEREUM
    assert Chain.ETHEREUM != Chain.ROPSTEN
