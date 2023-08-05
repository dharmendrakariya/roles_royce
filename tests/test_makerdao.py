from roles_royce import check, send, Chain
from roles_royce.protocols.eth import makerdao
from roles_royce.constants import ETHAddr

# Test safe
AVATAR = "0xC01318baB7ee1f5ba734172bF7718b5DC6Ec90E1"
ROLES_MOD_ADDRESS = "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86"
ROLE = 2

MAKERMANAGER = "0x5ef30b9986345249bc32d8928B7ee64DE9435E39"
DAIJOIN = "0x9759A6Ac90977b93B58547b4A71c78317f391A28"
WSTETHJOIN = "0x10CD5fbe1b404B7E19Ef964B63939907bdaf42E2"
VAULT = 27353



def test_approve_dai():
    request = makerdao.ApproveDAI(spender=AVATAR, amount=1_000)
    assert request.data == "0x095ea7b3000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e100000000000000000000000000000000000000000000000000000000000003e8"

def test_approve_wsteth():
    request = makerdao.ApproveWstETH(spender=AVATAR, amount=1_000)
    assert request.data == "0x095ea7b3000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e100000000000000000000000000000000000000000000000000000000000003e8"

def test_withdraw_collateral():
    request = makerdao.WithdrawCollateral(adapter=WSTETHJOIN, cdp_vault=VAULT, amount=1_000)
    assert request.data == "0x6ab6a4910000000000000000000000005ef30b9986345249bc32d8928b7ee64de9435e3900000000000000000000000010cd5fbe1b404b7e19ef964b63939907bdaf42e2" \
                            "0000000000000000000000000000000000000000000000000000000000006ad900000000000000000000000000000000000000000000000000000000000003e8"

def test_deposit_collateral():
    request = makerdao.DepositCollateral(adapter=WSTETHJOIN, cdp_vault=VAULT, amount=1_000)
    assert request.data == "0x3e29e5650000000000000000000000005ef30b9986345249bc32d8928b7ee64de9435e3900000000000000000000000010cd5fbe1b404b7e19ef964b63939907bdaf42e2" \
                            "0000000000000000000000000000000000000000000000000000000000006ad900000000000000000000000000000000000000000000000000000000000003e8" \
                            "0000000000000000000000000000000000000000000000000000000000000001"

def test_payback():
    request = makerdao.PayBack(adapter=DAIJOIN, cdp_vault=VAULT, amount=1_000)
    assert request.data == "0x4b6661990000000000000000000000005ef30b9986345249bc32d8928b7ee64de9435e390000000000000000000000009759a6ac90977b93b58547b4a71c78317f391a28" \
                            "0000000000000000000000000000000000000000000000000000000000006ad900000000000000000000000000000000000000000000000000000000000003e8"

def test_mint_dai():
    request = makerdao.MintDAI(adapter=DAIJOIN, cdp_vault=VAULT, amount=1_000)
    assert request.data == "0x9f6f3d5b0000000000000000000000005ef30b9986345249bc32d8928b7ee64de9435e3900000000000000000000000019c0976f590d67707e62397c87829d896dc0f1f1" \
                            "0000000000000000000000009759a6ac90977b93b58547b4a71c78317f391a280000000000000000000000000000000000000000000000000000000000006ad9" \
                            "00000000000000000000000000000000000000000000000000000000000003e8"

def test_payback_and_withdraw():
    request = makerdao.PayBackAndWithdrawCol(adapter=WSTETHJOIN, dai_join=DAIJOIN, cdp_vault=VAULT, amount=1_000)
    assert request.data == "0xbcd6deec0000000000000000000000005ef30b9986345249bc32d8928b7ee64de9435e3900000000000000000000000010cd5fbe1b404b7e19ef964b63939907bdaf42e2" \
                            "0000000000000000000000009759a6ac90977b93b58547b4a71c78317f391a280000000000000000000000000000000000000000000000000000000000006ad9" \
                            "00000000000000000000000000000000000000000000000000000000000003e8"

def test_undelegate_mkr():
    request = makerdao.UndelegateMKR(amount=6_000_000_000)
    assert request.data == "0xd8ccd0f30000000000000000000000000000000000000000000000000000000165a0bc00"

def test_delegate_mkr():
    request = makerdao.DelegateMKR(amount=6_000_000_000)
    assert request.data == "0xdd4670640000000000000000000000000000000000000000000000000000000165a0bc00"

def test_join_pot():
    request = makerdao.JoinPot(destination=AVATAR, amount=1_000)
    assert request.data == "0x3b4da69f000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e100000000000000000000000000000000000000000000000000000000000003e8"

def test_exit_pot():
    request = makerdao.ExitPot(destination=AVATAR, amount=1_000)
    assert request.data == "0xef693bed000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e100000000000000000000000000000000000000000000000000000000000003e8"

def test_drip_pot():
    request = makerdao.DripThePot()
    assert request.data == "0x9f678cca"