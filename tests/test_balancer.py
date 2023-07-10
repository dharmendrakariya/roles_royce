import pytest

from roles_royce import check, Chain
from roles_royce.protocols.eth import balancer

from .utils import web3_eth

bb_a_USD_pid = "0x32296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080"
avatar_address = '0x0bEcEb88bf999727F52f0f8EfeD66d92c089BD45'
roles_mod_address = '0xf20325cf84b72e8BBF8D8984B8f0059B984B390B'
asset1 = "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"
asset2 = "0x0000000000000000000000000000000000000000"
asset3 = "0xBA485b556399123261a5F9c95d413B4f93107407"


# pytestmark = pytest.mark.skip("all tests still WIP")

def test_exit_pool_single(web3_eth):
    assets = [asset1, asset2]
    bpt_amount_in = 16991614618808728544
    m = balancer.SingleAssetQueryExit(pool_id=bb_a_USD_pid,
                                      avatar=avatar_address,
                                      assets=assets,
                                      min_amounts_out=[0, 0],  # Not used
                                      bpt_amount_in=bpt_amount_in,
                                      exit_token_index=1)

    bpt_in, amounts_out = m.call(web3=web3_eth, block_identifier=17658530)
    assert bpt_in == bpt_amount_in
    assert amounts_out == [0, 17604819345413045908]

    # allow 1% slipage
    amounts_out = [int(amount * 0.99) for amount in amounts_out]

    m = balancer.SingleAssetExit(pool_id=bb_a_USD_pid,
                                 avatar=avatar_address,
                                 assets=assets,
                                 min_amounts_out=amounts_out,
                                 bpt_amount_in=bpt_in,
                                 exit_token_index=1)

    assert m.data == "0x8bdb391332296969ef14eb0c6d29669c550d4a04491302300002000000000000000000800000000000000000000000000be" \
                     "ceb88bf999727f52f0f8efed66d92c089bd450000000000000000000000000beceb88bf999727f52f0f8efed66d92c089bd45" \
                     "00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000" \
                     "00000000000000000000000008000000000000000000000000000000000000000000000000000000000000000e00000000000" \
                     "00000000000000000000000000000000000000000000000000014000000000000000000000000000000000000000000000000" \
                     "00000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000" \
                     "00007f39c581f595b53c5cb19bd0b3f8da6c935e2ca0000000000000000000000000000000000000000000000000000000000" \
                     "00000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000" \
                     "0000000000000000000000000000000000000000000000000000000000000000000000000000000000f1df6f0568163800000" \
                     "00000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000" \
                     "000000000000000000000000000000000000000000000000000000000000000000000000ebce57786a6dbbe00000000000000" \
                     "000000000000000000000000000000000000000000000000001"


def test_exit_pool_proportional():
    assets = [asset1, asset2, asset3]
    m = balancer.ProportionalExit(pool_id=bb_a_USD_pid,
                                  avatar=avatar_address,
                                  assets=assets,
                                  min_amounts_out=[475606, 50483596, 40479939274726666244],
                                  bpt_amount_in=10)
    assert m.data == "0x8bdb391332296969ef14eb0c6d29669c550d4a04491302300002000000000000000000800000000000000000000000000" \
                     "beceb88bf999727f52f0f8efed66d92c089bd450000000000000000000000000beceb88bf999727f52f0f8efed66d92c089" \
                     "bd4500000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000" \
                     "000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000010000" \
                     "000000000000000000000000000000000000000000000000000000000001800000000000000000000000000000000000000" \
                     "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300000000" \
                     "00000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca00000000000000000000000000000000000000000000" \
                     "000000000000000000000000000000000000000000000ba485b556399123261a5f9c95d413b4f9310740700000000000000" \
                     "000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000" \
                     "0000000000741d6000000000000000000000000000000000000000000000000000000000302518c00000000000000000000" \
                     "000000000000000000000000000231c5a24c677770040000000000000000000000000000000000000000000000000000000" \
                     "000000040000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000" \
                     "0000000000000000000000000000000000000a"


def test_exit_pool_custom():
    assets = [asset1, asset2, asset3]
    m = balancer.CustomExit(pool_id=bb_a_USD_pid,
                            avatar=avatar_address,
                            assets=assets,
                            amounts_out=[475606, 50483596, 40479939274726666244],
                            max_bpt_amount_in=1324647182609730135593)
    assert m.data == "0x8bdb391332296969ef14eb0c6d29669c550d4a04491302300002000000000000000000800000000000000000000000000" \
                     "beceb88bf999727f52f0f8efed66d92c089bd450000000000000000000000000beceb88bf999727f52f0f8efed66d92c089" \
                     "bd4500000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000" \
                     "000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000010000" \
                     "000000000000000000000000000000000000000000000000000000000001800000000000000000000000000000000000000" \
                     "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300000000" \
                     "00000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca00000000000000000000000000000000000000000000" \
                     "000000000000000000000000000000000000000000000ba485b556399123261a5f9c95d413b4f9310740700000000000000" \
                     "000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000" \
                     "0000000000741d6000000000000000000000000000000000000000000000000000000000302518c00000000000000000000" \
                     "000000000000000000000000000231c5a24c677770040000000000000000000000000000000000000000000000000000000" \
                     "0000000e0000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000" \
                     "00000000000000000000000000000000000060000000000000000000000000000000000000000000000047cf2c2a4d4ef66" \
                     "629000000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000" \
                     "000000000000000000000000000741d6000000000000000000000000000000000000000000000000000000000302518c000" \
                     "00000000000000000000000000000000000000000000231c5a24c67777004"


pool_id = "0x32296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080"
join_assets = ["0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0", "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"]
join_avatar_address = "0xB7eECEc62C5F7931C76b834B3126D70F0a7C28EE"


def test_join_pool_single(web3_eth):
    max_amounts_in = [45570785292221453624530, 4758711463074243205157]
    m = balancer.SingleAssetJoin(pool_id=pool_id,
                                 avatar=join_avatar_address,
                                 assets=join_assets,
                                 max_amounts_in=max_amounts_in,
                                 bpt_amount_out=9566160736748514880352,
                                 join_token_index=1)
    assert m.data == "0xb95cac2832296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080000000000000000000000000" \
                     "b7eecec62c5f7931c76b834b3126d70f0a7c28ee000000000000000000000000b7eecec62c5f7931c76b834b3126d70f0a" \
                     "7c28ee00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000" \
                     "00000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000" \
                     "e0000000000000000000000000000000000000000000000000000000000000014000000000000000000000000000000000" \
                     "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200" \
                     "00000000000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca0000000000000000000000000c02aaa39b223" \
                     "fe8d0a0e5c4f27ead9083c756cc20000000000000000000000000000000000000000000000000000000000000002000000" \
                     "0000000000000000000000000000000000000000f70a2b39e417e9fed20000000000000000000000000000000000000000" \
                     "00000101f8634eee9faad82500000000000000000000000000000000000000000000000000000000000000600000000000" \
                     "00000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000" \
                     "020695261a61884cab600000000000000000000000000000000000000000000000000000000000000001"


def test_join_pool_proportional():
    m = balancer.ProportionalJoin(pool_id=pool_id,
                                  avatar=join_avatar_address,
                                  assets=join_assets,
                                  max_amounts_in=[4557078529222453624530, 4758711463074243205157],
                                  bpt_amount_out=9566160736748514880352)
    assert m.data == "0xb95cac2832296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080000000000000000000000000" \
                     "b7eecec62c5f7931c76b834b3126d70f0a7c28ee000000000000000000000000b7eecec62c5f7931c76b834b3126d70f0a" \
                     "7c28ee00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000" \
                     "00000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000" \
                     "e0000000000000000000000000000000000000000000000000000000000000014000000000000000000000000000000000" \
                     "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200" \
                     "00000000000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca0000000000000000000000000c02aaa39b223" \
                     "fe8d0a0e5c4f27ead9083c756cc20000000000000000000000000000000000000000000000000000000000000002000000" \
                     "0000000000000000000000000000000000000000f70a2b39e417e9fed20000000000000000000000000000000000000000" \
                     "00000101f8634eee9faad82500000000000000000000000000000000000000000000000000000000000000400000000000" \
                     "00000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000" \
                     "020695261a61884cab60"


def test_join_pool_exact(web3_eth):
    assets = [asset1, asset2]
    amounts_in = [0, 17604819345413045908]
    m = balancer.ExactAssetQueryJoin(pool_id=bb_a_USD_pid,
                                      avatar=avatar_address,
                                      assets=assets,
                                      amounts_in=amounts_in,
                                      min_bpt_out=0, # Not used
                                    )

    bpt_out, amounts_in = m.call(web3=web3_eth, block_identifier=17658530)
    assert bpt_out == 16984717609097619472
    assert amounts_in == amounts_in

    # allow 1% slipage
    min_bpt_out = int(bpt_out * 0.99)


    m = balancer.ExactTokensJoin(pool_id=pool_id,
                                 avatar=join_avatar_address,
                                 assets=join_assets,
                                 amounts_in=[4557078529222453624530, 4758711463074243205157],
                                 min_bpt_out=min_bpt_out)
    assert m.data =="0xb95cac2832296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080000000000000000000000000" \
                    "b7eecec62c5f7931c76b834b3126d70f0a7c28ee000000000000000000000000b7eecec62c5f7931c76b834b3126d70f0a" \
                    "7c28ee00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000" \
                    "00000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000" \
                    "e0000000000000000000000000000000000000000000000000000000000000014000000000000000000000000000000000" \
                    "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200" \
                    "00000000000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca0000000000000000000000000c02aaa39b223" \
                    "fe8d0a0e5c4f27ead9083c756cc20000000000000000000000000000000000000000000000000000000000000002000000" \
                    "0000000000000000000000000000000000000000f70a2b39e417e9fed20000000000000000000000000000000000000000" \
                    "00000101f8634eee9faad82500000000000000000000000000000000000000000000000000000000000000c00000000000" \
                    "00000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000" \
                    "00000000000000000060000000000000000000000000000000000000000000000000e95a6b91df94680000000000000000" \
                    "000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000f7" \
                    "0a2b39e417e9fed2000000000000000000000000000000000000000000000101f8634eee9faad825"
