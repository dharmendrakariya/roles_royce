from defabipedia.types import Chain

from roles_royce.protocols.swap_pools import swap_methods

TOKEN_X = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
TOKEN_Y = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
AMOUNT_X = 1_000_000_000_000_000_000_000
MIN_AMOUNT_Y = 0
DEADLINE = 1_000_000_000_000


def test_swap_curve():
    method = swap_methods.SwapCurve(
        blockchain=Chain.ETHEREUM,
        pool_address="0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51",
        token_x=0,
        token_y=1,
        amount_x=AMOUNT_X,
        min_amount_y=MIN_AMOUNT_Y,
    )
    assert method.target_address == "0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51"
    assert (
        method.data
        == "0x3df021240000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000003635c9adc5dea000000000000000000000000000000000000000000000000000000000000000000000"
    )


def test_swap_uniswap_v3():
    method = swap_methods.SwapUniswapV3(
        blockchain=Chain.ETHEREUM,
        token_in=TOKEN_X,
        token_out=TOKEN_Y,
        avatar="0x849D52316331967b6fF1198e5E32A0eB168D039d",
        deadline=DEADLINE,
        amount_in=AMOUNT_X,
        min_amount_out=MIN_AMOUNT_Y,
    )
    assert method.args_list == [
        (
            "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            100,
            "0x849D52316331967b6fF1198e5E32A0eB168D039d",
            1000000000000,
            1000000000000000000000,
            0,
            0,
        )
    ]
    assert (
        method.data
        == "0x414bf389000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec70000000000000000000000000000000000000000000000000000000000000064000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d000000000000000000000000000000000000000000000000000000e8d4a5100000000000000000000000000000000000000000000000003635c9adc5dea0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    )
