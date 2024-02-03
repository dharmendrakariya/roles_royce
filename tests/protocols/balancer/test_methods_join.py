from roles_royce.protocols import balancer
from ...utils import local_node_eth


stable_pool_pid = "0x3dd0843a028c86e0b760b1a76929d1c5ef93a2dd000200000000000000000249"
metastable_pool_pid = "0x1e19cf2d73a72ef1332c882f20534b6519be0276000200000000000000000112"
composable_stable_pool_pid = "0x42ed016f826165c2e5976fe5bc3df540c5ad0af700000000000000000000058b"
weighted_pool_pid = "0x5c6ee304399dbdb9c8ef030ab642b10820db8f56000200000000000000000014"

bb_a_USD_pid = "0x32296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080"

avatar_address = '0x0bEcEb88bf999727F52f0f8EfeD66d92c089BD45'
roles_mod_address = '0xf20325cf84b72e8BBF8D8984B8f0059B984B390B'
asset1 = "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"
asset2 = "0x0000000000000000000000000000000000000000"
asset3 = "0xBA485b556399123261a5F9c95d413B4f93107407"

block = 17658530
block_composable = 18238491

pool_id = "0x32296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080"
join_assets = ["0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0", "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"]
join_avatar_address = "0xB7eECEc62C5F7931C76b834B3126D70F0a7C28EE"

#@pytest.mark.skip("WIP")
def test_join_pool_exact_tokens(local_node_eth):
    w3 = local_node_eth.w3
    local_node_eth.set_block(block)

    amounts_in = [166666789, 17604819345413045908]
    m = balancer.ExactTokensQueryJoin(w3=w3,
                                      pool_id=bb_a_USD_pid,
                                      amounts_in=amounts_in)

    bpt_out, amounts_in = m.call(web3=w3, block_identifier=17658530)
    assert bpt_out == 16984717609279605576
    assert amounts_in == amounts_in

    # allow 1% slippage
    min_bpt_amount_out = int(bpt_out * 0.99)

    m = balancer.ExactTokensJoin(w3=w3,
                                 pool_id=pool_id,
                                 avatar=join_avatar_address,
                                 amounts_in=[4557078529222453624530, 4758711463074243205157],
                                 min_bpt_amount_out=min_bpt_amount_out)

    assert m.data == "0xb95cac2832296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080000000000000000000000000b7eecec62c5f7931c76b834b3126d70f0a7c28ee000000000000000000000000b7eecec62c5f7931c76b834b3126d70f0a7c28ee0000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000e00000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca0000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000f70a2b39e417e9fed2000000000000000000000000000000000000000000000101f8634eee9faad82500000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000e95a6b91ea51800000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000f70a2b39e417e9fed2000000000000000000000000000000000000000000000101f8634eee9faad825"

