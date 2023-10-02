from roles_royce.protocols.eth import maker
from .utils import (local_node, accounts, get_balance, steal_token, create_simple_safe)
from .roles import setup_common_roles, deploy_roles, apply_presets
from roles_royce import roles
from roles_royce.constants import ETHAddr
from decimal import Decimal
from pytest import approx

wstETH_JOIN = "0x10CD5fbe1b404B7E19Ef964B63939907bdaf42E2" # GemJoin wstETH
ABI_GEM_JOIN = '[{"constant":true,"inputs":[],"name":"gem","outputs":[{"internalType":"contract GemLike_3","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"ilk","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"}]'
ABI_TOKEN = '[{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
ABI_CDP_MANAGER = '[{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"urns","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]'
ABI_VAT = '[{"constant":true,"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"address","name":"","type":"address"}],"name":"urns","outputs":[{"internalType":"uint256","name":"ink","type":"uint256"},{"internalType":"uint256","name":"art","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"ilks","outputs":[{"internalType":"uint256","name":"Art","type":"uint256"},{"internalType":"uint256","name":"rate","type":"uint256"},{"internalType":"uint256","name":"spot","type":"uint256"},{"internalType":"uint256","name":"line","type":"uint256"},{"internalType":"uint256","name":"dust","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"dai","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'
ABI_JUG = '[{"constant":false,"inputs":[{"internalType":"bytes32","name":"ilk","type":"bytes32"}],"name":"drip","outputs":[{"internalType":"uint256","name":"rate","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
ABI_ROLES = '[{"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"address","name":"_avatar","type":"address"},{"internalType":"address","name":"_target","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ArraysDifferentLength","type":"error"},{"inputs":[],"name":"ModuleTransactionFailed","type":"error"},{"inputs":[],"name":"NoMembership","type":"error"},{"inputs":[],"name":"SetUpModulesAlreadyCalled","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"},{"indexed":false,"internalType":"uint16[]","name":"roles","type":"uint16[]"},{"indexed":false,"internalType":"bool[]","name":"memberOf","type":"bool[]"}],"name":"AssignRoles","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousAvatar","type":"address"},{"indexed":true,"internalType":"address","name":"newAvatar","type":"address"}],"name":"AvatarSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"guard","type":"address"}],"name":"ChangedGuard","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"}],"name":"DisabledModule","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"}],"name":"EnabledModule","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"initiator","type":"address"},{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"avatar","type":"address"},{"indexed":false,"internalType":"address","name":"target","type":"address"}],"name":"RolesModSetup","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"},{"indexed":false,"internalType":"uint16","name":"defaultRole","type":"uint16"}],"name":"SetDefaultRole","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"multisendAddress","type":"address"}],"name":"SetMultisendAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousTarget","type":"address"},{"indexed":true,"internalType":"address","name":"newTarget","type":"address"}],"name":"TargetSet","type":"event"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"enum ExecutionOptions","name":"options","type":"uint8"}],"name":"allowTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"module","type":"address"},{"internalType":"uint16[]","name":"_roles","type":"uint16[]"},{"internalType":"bool[]","name":"memberOf","type":"bool[]"}],"name":"assignRoles","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"avatar","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"defaultRoles","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prevModule","type":"address"},{"internalType":"address","name":"module","type":"address"}],"name":"disableModule","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"module","type":"address"}],"name":"enableModule","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"}],"name":"execTransactionFromModule","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"}],"name":"execTransactionFromModuleReturnData","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"},{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"bool","name":"shouldRevert","type":"bool"}],"name":"execTransactionWithRole","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"},{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"bool","name":"shouldRevert","type":"bool"}],"name":"execTransactionWithRoleReturnData","outputs":[{"internalType":"bool","name":"success","type":"bool"},{"internalType":"bytes","name":"returnData","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getGuard","outputs":[{"internalType":"address","name":"_guard","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"start","type":"address"},{"internalType":"uint256","name":"pageSize","type":"uint256"}],"name":"getModulesPaginated","outputs":[{"internalType":"address[]","name":"array","type":"address[]"},{"internalType":"address","name":"next","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"guard","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_module","type":"address"}],"name":"isModuleEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"multisend","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"}],"name":"revokeTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"enum ExecutionOptions","name":"options","type":"uint8"}],"name":"scopeAllowFunction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"bool[]","name":"isParamScoped","type":"bool[]"},{"internalType":"enum ParameterType[]","name":"paramType","type":"uint8[]"},{"internalType":"enum Comparison[]","name":"paramComp","type":"uint8[]"},{"internalType":"bytes[]","name":"compValue","type":"bytes[]"},{"internalType":"enum ExecutionOptions","name":"options","type":"uint8"}],"name":"scopeFunction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"enum ExecutionOptions","name":"options","type":"uint8"}],"name":"scopeFunctionExecutionOptions","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"uint256","name":"paramIndex","type":"uint256"},{"internalType":"enum ParameterType","name":"paramType","type":"uint8"},{"internalType":"enum Comparison","name":"paramComp","type":"uint8"},{"internalType":"bytes","name":"compValue","type":"bytes"}],"name":"scopeParameter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"uint256","name":"paramIndex","type":"uint256"},{"internalType":"enum ParameterType","name":"paramType","type":"uint8"},{"internalType":"bytes[]","name":"compValues","type":"bytes[]"}],"name":"scopeParameterAsOneOf","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"}],"name":"scopeRevokeFunction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"}],"name":"scopeTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_avatar","type":"address"}],"name":"setAvatar","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"module","type":"address"},{"internalType":"uint16","name":"role","type":"uint16"}],"name":"setDefaultRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_guard","type":"address"}],"name":"setGuard","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_multisend","type":"address"}],"name":"setMultisend","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_target","type":"address"}],"name":"setTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"initParams","type":"bytes"}],"name":"setUp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"target","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"uint8","name":"paramIndex","type":"uint8"}],"name":"unscopeParameter","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
ABI_POT = '[{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"pie","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"chi","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'
ABI_DSR_MANAGER = '[{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"pieOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'


def test_integration_maker_cdp_module_proxy(local_node, accounts):
    w3 = local_node
    safe = create_simple_safe(w3=w3, owner=accounts[0])
    roles_ctract = deploy_roles(avatar=safe.address, w3=w3)
    setup_common_roles(safe, roles_ctract)

    # Build proxy
    build_receipt = safe.send([maker.Build()]).receipt
    for log in build_receipt["logs"]:
        if log["topics"][0].hex() == "0x259b30ca39885c6d801a0b5dbc988640f3c25e2f37531fe138c5c5af8955d41b": # Created
            proxy_address = w3.to_checksum_address('0x' + log["data"].hex()[26:66])
            break

    gem_join_contract = w3.eth.contract(address=wstETH_JOIN, abi=ABI_GEM_JOIN)
    gem = gem_join_contract.functions.gem().call()
    ilk = gem_join_contract.functions.ilk().call()

    presets = """{"version": "1.0","chainId": "1","meta":{ "description": "","txBuilderVersion": "1.8.0"},"createdAt": 1695904723785,"transactions": [
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e82669500000000000000000000000000000000000000000000000000000000000000010000000000000000000000006b175474e89094c44da98b954eedeac495271d0f","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c00000000000000000000000000000000000000000000000000000000000000010000000000000000000000006b175474e89094c44da98b954eedeac495271d0f095ea7b30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000d758500ddec05172aaa035911387c8e0e789cf6a","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e8266950000000000000000000000000000000000000000000000000000000000000001000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2095ea7b30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000d758500ddec05172aaa035911387c8e0e789cf6a","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e8266950000000000000000000000000000000000000000000000000000000000000001000000000000000000000000d758500ddec05172aaa035911387c8e0e789cf6a","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000d758500ddec05172aaa035911387c8e0e789cf6a1cff79cd0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000002000000000000000000000000082ecd135dce65fbc6dbdd0e4237e0af93ffd5038","value": "0"}
    ]}"""
    apply_presets(safe, roles_ctract, json_data=presets, replaces=[("c01318bab7ee1f5ba734172bf7718b5dc6ec90e1", safe.address[2:]), ("c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", gem[2:]), ("d758500ddec05172aaa035911387c8e0e789cf6a", proxy_address[2:])])

    # steal wstETH
    steal_token(w3, token=ETHAddr.wstETH, holder="0x6cE0F913F035ec6195bC3cE885aec4C66E485BC4",
                to=safe.address, amount=1000_000_000_000_000_000_000)
    # approve gem
    approve_gem = maker.ApproveGem(gem=gem, spender=proxy_address, amount=1000_000_000_000_000_000_000)
    roles.send([approve_gem], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    
    gem_contract = w3.eth.contract(address=gem, abi=ABI_TOKEN)
    gem_allowance = gem_contract.functions.allowance(safe.address, proxy_address).call()
    assert gem_allowance == 1000_000_000_000_000_000_000

    # open cdp
    open_cdp = maker.ProxyActionOpen(proxy=proxy_address, ilk=ilk)
    send_open_cdp = roles.send([open_cdp], role=1, private_key=accounts[1].key,
                                roles_mod_address=roles_ctract.address,
                                web3=w3)

    cdp_id = None
    for log in send_open_cdp["logs"]:
        if log["topics"][0].hex() == "0xd6be0bc178658a382ff4f91c8c68b542aa6b71685b8fe427966b87745c3ea7a2": # NewCdp
            cdp_id = int(log["topics"][3].hex(), 16)
            # print('CDP ID: ', cdp_id)
            break
    
    assert cdp_id

    # lockGem
    lock_gem = maker.ProxyActionLockGem(proxy=proxy_address, gem_join=wstETH_JOIN, cdp_id=cdp_id, wad=1000_000_000_000_000_000_000)
    roles.send([lock_gem], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    cdp_manager_contract = w3.eth.contract(address=ETHAddr.MakerCDPManager, abi=ABI_CDP_MANAGER)
    urn_handler = cdp_manager_contract.functions.urns(cdp_id).call()
    vat_contract = w3.eth.contract(address=ETHAddr.MakerVat, abi=ABI_VAT)
    locked_gem = vat_contract.functions.urns(ilk, urn_handler).call()[0]
    assert locked_gem == 1000_000_000_000_000_000_000

    # draw DAI
    draw_dai = maker.ProxyActionDraw(proxy=proxy_address, cdp_id=cdp_id, wad=100_000_000_000_000_000_000_000)
    roles.send([draw_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_balance = get_balance(w3=w3, token=ETHAddr.DAI, address=safe.address)
    assert dai_balance == 100_000_000_000_000_000_000_000

    # approve DAI
    approve_dai = maker.ApproveDAI(spender=proxy_address, amount=100_000_000_000_000_000_000_000)
    roles.send([approve_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_contract = w3.eth.contract(address=ETHAddr.DAI, abi=ABI_TOKEN)
    dai_allowance = dai_contract.functions.allowance(safe.address, proxy_address).call()
    assert dai_allowance == 100_000_000_000_000_000_000_000

    # wipe DAI
    wipe_dai = maker.ProxyActionWipe(proxy=proxy_address, cdp_id=cdp_id, wad=100_000_000_000_000_000_000_000)
    roles.send([wipe_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_balance = get_balance(w3=w3, token=ETHAddr.DAI, address=safe.address)
    assert dai_balance == 0

    # freeGem
    free_gem = maker.ProxyActionFreeGem(proxy=proxy_address, gem_join=wstETH_JOIN, cdp_id=cdp_id, wad=1000_000_000_000_000_000_000)
    roles.send([free_gem], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    locked_gem = vat_contract.functions.urns(ilk, urn_handler).call()[0]
    assert locked_gem == 0


def test_integration_maker_cdp_module_no_proxy(local_node, accounts):
    w3 = local_node
    safe = create_simple_safe(w3=w3, owner=accounts[0])
    roles_ctract = deploy_roles(avatar=safe.address, w3=w3)
    setup_common_roles(safe, roles_ctract)

    gem_join_contract = w3.eth.contract(address=wstETH_JOIN, abi=ABI_GEM_JOIN)
    gem = gem_join_contract.functions.gem().call()
    ilk = gem_join_contract.functions.ilk().call()

    presets = """{"version": "1.0","chainId": "1","meta":{ "description": "","txBuilderVersion": "1.8.0"},"createdAt": 1695904723785,"transactions": [
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e82669500000000000000000000000000000000000000000000000000000000000000010000000000000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca0","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c00000000000000000000000000000000000000000000000000000000000000010000000000000000000000007f39c581f595b53c5cb19bd0b3f8da6c935e2ca0095ea7b30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000002000000000000000000000000010cd5fbe1b404b7e19ef964b63939907bdaf42e2","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e82669500000000000000000000000000000000000000000000000000000000000000010000000000000000000000006b175474e89094c44da98b954eedeac495271d0f","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c00000000000000000000000000000000000000000000000000000000000000010000000000000000000000006b175474e89094c44da98b954eedeac495271d0f095ea7b30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000200000000000000000000000009759a6ac90977b93b58547b4a71c78317f391a28","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e82669500000000000000000000000000000000000000000000000000000000000000010000000000000000000000005ef30b9986345249bc32d8928b7ee64de9435e39","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c00000000000000000000000000000000000000000000000000000000000000010000000000000000000000005ef30b9986345249bc32d8928b7ee64de9435e396090dec5000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000220000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e1","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x2fcf52d100000000000000000000000000000000000000000000000000000000000000010000000000000000000000005ef30b9986345249bc32d8928b7ee64de9435e3945e6bdcd000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x2fcf52d100000000000000000000000000000000000000000000000000000000000000010000000000000000000000005ef30b9986345249bc32d8928b7ee64de9435e39f9f30db6000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c00000000000000000000000000000000000000000000000000000000000000010000000000000000000000005ef30b9986345249bc32d8928b7ee64de9435e399bb8f838000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000220000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e1","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e826695000000000000000000000000000000000000000000000000000000000000000100000000000000000000000010cd5fbe1b404b7e19ef964b63939907bdaf42e2","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x2fcf52d1000000000000000000000000000000000000000000000000000000000000000100000000000000000000000010cd5fbe1b404b7e19ef964b63939907bdaf42e23b4da69f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c000000000000000000000000000000000000000000000000000000000000000100000000000000000000000010cd5fbe1b404b7e19ef964b63939907bdaf42e2ef693bed0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e1","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e82669500000000000000000000000000000000000000000000000000000000000000010000000000000000000000009759a6ac90977b93b58547b4a71c78317f391a28","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x2fcf52d100000000000000000000000000000000000000000000000000000000000000010000000000000000000000009759a6ac90977b93b58547b4a71c78317f391a283b4da69f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c00000000000000000000000000000000000000000000000000000000000000010000000000000000000000009759a6ac90977b93b58547b4a71c78317f391a28ef693bed0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e1","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e826695000000000000000000000000000000000000000000000000000000000000000100000000000000000000000019c0976f590d67707e62397c87829d896dc0f1f1","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x2fcf52d1000000000000000000000000000000000000000000000000000000000000000100000000000000000000000019c0976f590d67707e62397c87829d896dc0f1f144e2a5a8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e826695000000000000000000000000000000000000000000000000000000000000000100000000000000000000000035d1b3f3d7966a1dfe207aa4514c12a259a0492b","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c000000000000000000000000000000000000000000000000000000000000000100000000000000000000000035d1b3f3d7966a1dfe207aa4514c12a259a0492ba3b22fc40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000200000000000000000000000009759a6ac90977b93b58547b4a71c78317f391a28","value": "0"}
    ]}"""
    apply_presets(safe, roles_ctract, json_data=presets, replaces=[("c01318bab7ee1f5ba734172bf7718b5dc6ec90e1", safe.address[2:]), ("7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0", gem[2:]), ("10cd5fbe1b404b7e19ef964b63939907bdaf42e2", gem_join_contract.address[2:])])

    # steal wstETH
    steal_token(w3, token=ETHAddr.wstETH, holder="0x6cE0F913F035ec6195bC3cE885aec4C66E485BC4",
                to=safe.address, amount=1000_000_000_000_000_000_000)
    # approve gem
    approve_gem = maker.ApproveGem(gem=gem, spender=gem_join_contract.address, amount=1000_000_000_000_000_000_000)
    roles.send([approve_gem], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    
    gem_contract = w3.eth.contract(address=gem, abi=ABI_TOKEN)
    gem_allowance = gem_contract.functions.allowance(safe.address, gem_join_contract.address).call()
    assert gem_allowance == 1000_000_000_000_000_000_000
    
    # open cdp
    open_cdp = maker.Open(ilk=ilk, avatar=safe.address)
    send_open_cdp = roles.send([open_cdp], role=1, private_key=accounts[1].key,
                                roles_mod_address=roles_ctract.address,
                                web3=w3)

    cdp_id = None
    for log in send_open_cdp["logs"]:
        if log["topics"][0].hex() == "0xd6be0bc178658a382ff4f91c8c68b542aa6b71685b8fe427966b87745c3ea7a2": # NewCdp
            cdp_id = int(log["topics"][3].hex(), 16)
            # print('CDP ID: ', cdp_id)
            break
    
    assert cdp_id

    # lockGem
    wad_gem = 1000_000_000_000_000_000_000
    cdp_manager_contract = w3.eth.contract(address=ETHAddr.MakerCDPManager, abi=ABI_CDP_MANAGER)
    urn_handler = cdp_manager_contract.functions.urns(cdp_id).call()
    join_lock_gem = maker.Join(assetJoin=gem_join_contract.address, usr=urn_handler, wad=wad_gem)
    roles.send([join_lock_gem], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    frob_lock_gem = maker.Frob(cdp_id=cdp_id, dink=wad_gem, dart=0)
    roles.send([frob_lock_gem], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    vat_contract = w3.eth.contract(address=ETHAddr.MakerVat, abi=ABI_VAT)
    locked_gem = vat_contract.functions.urns(ilk, urn_handler).call()[0]
    assert locked_gem == wad_gem

    # draw DAI
    RAY = 10**27
    wad_dai = 100_000_000_000_000_000_000_000
    jug_contract = w3.eth.contract(address=ETHAddr.MakerJug, abi=ABI_JUG)
    drip = maker.Drip(ilk=ilk)
    roles.send([drip], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    rate_jug = jug_contract.functions.drip(ilk).call()
    rate_vat = vat_contract.functions.ilks(ilk).call()[1]
    assert rate_jug == rate_vat

    urn_dai = vat_contract.functions.dai(urn_handler).call()

    if urn_dai < (RAY * wad_dai):
        dart = int(((Decimal(RAY) * Decimal(wad_dai)) - urn_dai) / Decimal(rate_jug))
        if dart * rate_jug < RAY * wad_dai:
            dart += 1
    
    frob_draw = maker.Frob(cdp_id=cdp_id, dink=0, dart=dart)
    roles.send([frob_draw], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    # variable that has 45 decimal places
    rad = wad_dai * 10**27 # 45 = 18 + 27
    move = maker.Move(cdp_id=cdp_id, avatar=safe.address, rad=rad)
    roles.send([move], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    hope = maker.Hope()
    roles.send([hope], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    exit_draw = maker.Exit(assetJoin=ETHAddr.MakerDaiJoin, avatar=safe.address, wad=wad_dai)
    roles.send([exit_draw], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_balance = get_balance(w3=w3, token=ETHAddr.DAI, address=safe.address)
    assert dai_balance == wad_dai

    # wipeDAI / repayDAI
    wad_dai = 50_000_000_000_000_000_000_000
    approve_dai = maker.ApproveDAI(spender=ETHAddr.MakerDaiJoin, amount=wad_dai)
    roles.send([approve_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    join_wipe = maker.Join(assetJoin=ETHAddr.MakerDaiJoin, usr=urn_handler, wad=wad_dai)
    roles.send([join_wipe], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    rate = vat_contract.functions.ilks(ilk).call()[1]
    art = vat_contract.functions.urns(ilk, urn_handler).call()[1]
    urn_dai = vat_contract.functions.dai(urn_handler).call()

    dart = int(Decimal(urn_dai) / Decimal(rate))
    if dart < art:
        dart = -dart
    else:
        dart = -int(art)
    
    frob_wipe = maker.Frob(cdp_id=cdp_id, dink=0, dart=dart)
    roles.send([frob_wipe], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_balance = get_balance(w3=w3, token=ETHAddr.DAI, address=safe.address)
    assert dai_balance == wad_dai

    # wipeAll / repayAllDAI
    rate = vat_contract.functions.ilks(ilk).call()[1]
    art = vat_contract.functions.urns(ilk, urn_handler).call()[1]
    urn_dai = vat_contract.functions.dai(urn_handler).call()
    rad = int((Decimal(art) * Decimal(rate)) - Decimal(urn_dai))
    wad_dai = int(Decimal(rad) / Decimal(RAY))

    if (wad_dai * RAY) < rad:
        wad_dai += 1

    approve_dai = maker.ApproveDAI(spender=ETHAddr.MakerDaiJoin, amount=wad_dai)
    roles.send([approve_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    join_wipe_all = maker.Join(assetJoin=ETHAddr.MakerDaiJoin, usr=urn_handler, wad=wad_dai)
    roles.send([join_wipe_all], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    art = vat_contract.functions.urns(ilk, urn_handler).call()[1]
    frob_wipe_all = maker.Frob(cdp_id=cdp_id, dink=0, dart=-art)
    roles.send([frob_wipe_all], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_balance = get_balance(w3=w3, token=ETHAddr.DAI, address=safe.address)
    assert dai_balance == 0

    # freeGem
    wad_gem = 1000_000_000_000_000_000_000
    frob_free_gem = maker.Frob(cdp_id=cdp_id, dink=-wad_gem, dart=0)
    roles.send([frob_free_gem], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    flux = maker.Flux(cdp_id=cdp_id, avatar=safe.address, wad=wad_gem)
    roles.send([flux], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    exit_free_gem = maker.Exit(assetJoin=gem_join_contract.address, avatar=safe.address, wad=wad_gem)
    roles.send([exit_free_gem], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    locked_gem = vat_contract.functions.urns(ilk, urn_handler).call()[0]
    gem_balance = get_balance(w3=w3, token=gem, address=safe.address)
    assert locked_gem == 0
    assert gem_balance == wad_gem

def test_integration_maker_dsr_module_proxy(local_node, accounts):
    w3 = local_node
    safe = create_simple_safe(w3=w3, owner=accounts[0])
    roles_ctract = deploy_roles(avatar=safe.address, w3=w3)
    setup_common_roles(safe, roles_ctract)

    # Build proxy
    build_receipt = safe.send([maker.Build()]).receipt
    for log in build_receipt["logs"]:
        if log["topics"][0].hex() == "0x259b30ca39885c6d801a0b5dbc988640f3c25e2f37531fe138c5c5af8955d41b": # Created
            proxy_address = w3.to_checksum_address('0x' + log["data"].hex()[26:66])
            break

    presets = """{"version": "1.0","chainId": "1","meta":{ "description": "","txBuilderVersion": "1.8.0"},"createdAt": 1695904723785,"transactions": [
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e82669500000000000000000000000000000000000000000000000000000000000000010000000000000000000000006b175474e89094c44da98b954eedeac495271d0f","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c00000000000000000000000000000000000000000000000000000000000000010000000000000000000000006b175474e89094c44da98b954eedeac495271d0f095ea7b30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000d758500ddec05172aaa035911387c8e0e789cf6a","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e8266950000000000000000000000000000000000000000000000000000000000000001000000000000000000000000d758500ddec05172aaa035911387c8e0e789cf6a","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000d758500ddec05172aaa035911387c8e0e789cf6a1cff79cd0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000002000000000000000000000000007ee93aeea0a36fff2a9b95dd22bd6049ee54f26","value": "0"}
    ]}"""
    apply_presets(safe, roles_ctract, json_data=presets, replaces=[("c01318bab7ee1f5ba734172bf7718b5dc6ec90e1", safe.address[2:]), ("d758500ddec05172aaa035911387c8e0e789cf6a", proxy_address[2:])])

    # steal DAI
    steal_token(w3, token=ETHAddr.DAI, holder="0x60FaAe176336dAb62e284Fe19B885B095d29fB7F",
                to=safe.address, amount=100_000_000_000_000_000_000_000)
    
    pot_contract = w3.eth.contract(address=ETHAddr.MakerPot, abi=ABI_POT)

    # approve DAI
    approve_dai = maker.ApproveDAI(spender=proxy_address, amount=100_000_000_000_000_000_000_000)
    roles.send([approve_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_contract = w3.eth.contract(address=ETHAddr.DAI, abi=ABI_TOKEN)
    dai_allowance = dai_contract.functions.allowance(safe.address, proxy_address).call()
    assert dai_allowance == 100_000_000_000_000_000_000_000

    # join DAI
    join_dai = maker.ProxyActionJoinDrs(proxy=proxy_address, wad=100_000_000_000_000_000_000_000)
    roles.send([join_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_balance = get_balance(w3=w3, token=ETHAddr.DAI, address=safe.address)
    assert dai_balance == 0
    pie = pot_contract.functions.pie(proxy_address).call()
    chi = pot_contract.functions.chi().call() / (10**27)
    assert pie * chi == approx(100_000_000_000_000_000_000_000)

    # exit DAI
    exit_dai = maker.ProxyActionExitDsr(proxy=proxy_address, wad=50_000_000_000_000_000_000_000)
    roles.send([exit_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_balance = get_balance(w3=w3, token=ETHAddr.DAI, address=safe.address)
    assert dai_balance == approx(50_000_000_000_000_000_000_000)
    pie = pot_contract.functions.pie(proxy_address).call()
    chi = pot_contract.functions.chi().call() / (10**27)
    assert pie * chi == approx(50_000_000_000_000_000_000_000)

    # exitAll DAI
    exit_all_dai = maker.ProxyActionExitAllDsr(proxy=proxy_address)
    roles.send([exit_all_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_balance = get_balance(w3=w3, token=ETHAddr.DAI, address=safe.address)
    assert dai_balance == approx(100_000_000_000_000_000_000_000)
    pie = pot_contract.functions.pie(proxy_address).call()
    assert pie == 0

def test_integration_maker_dsr_module_no_proxy(local_node, accounts):
    w3 = local_node
    safe = create_simple_safe(w3=w3, owner=accounts[0])
    roles_ctract = deploy_roles(avatar=safe.address, w3=w3)
    setup_common_roles(safe, roles_ctract)

    presets = """{"version": "1.0","chainId": "1","meta":{ "description": "","txBuilderVersion": "1.8.0"},"createdAt": 1695904723785,"transactions": [
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e82669500000000000000000000000000000000000000000000000000000000000000010000000000000000000000006b175474e89094c44da98b954eedeac495271d0f","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c00000000000000000000000000000000000000000000000000000000000000010000000000000000000000006b175474e89094c44da98b954eedeac495271d0f095ea7b30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000373238337bfe1146fb49989fc222523f83081ddb","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x5e8266950000000000000000000000000000000000000000000000000000000000000001000000000000000000000000373238337bfe1146fb49989fc222523f83081ddb","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000373238337bfe1146fb49989fc222523f83081ddb3b4da69f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e1","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000373238337bfe1146fb49989fc222523f83081ddbef693bed0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e1","value": "0"},
    {"to": "0x1ffAdc16726dd4F91fF275b4bF50651801B06a86","data": "0x33a0480c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000373238337bfe1146fb49989fc222523f83081ddbeb0dff660000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000c01318bab7ee1f5ba734172bf7718b5dc6ec90e1","value": "0"}
    ]}"""
    apply_presets(safe, roles_ctract, json_data=presets, replaces=[("c01318bab7ee1f5ba734172bf7718b5dc6ec90e1", safe.address[2:])])

    # steal DAI
    steal_token(w3, token=ETHAddr.DAI, holder="0x60FaAe176336dAb62e284Fe19B885B095d29fB7F",
                to=safe.address, amount=100_000_000_000_000_000_000_000)
    
    dsr_manager_contract = w3.eth.contract(address=ETHAddr.MakerDSRManager, abi=ABI_DSR_MANAGER)
    pot_contract = w3.eth.contract(address=ETHAddr.MakerPot, abi=ABI_POT)

    # approve DAI
    approve_dai = maker.ApproveDAI(spender=ETHAddr.MakerDSRManager, amount=100_000_000_000_000_000_000_000)
    roles.send([approve_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_contract = w3.eth.contract(address=ETHAddr.DAI, abi=ABI_TOKEN)
    dai_allowance = dai_contract.functions.allowance(safe.address, ETHAddr.MakerDSRManager).call()
    assert dai_allowance == 100_000_000_000_000_000_000_000

    # join DAI
    join_dai = maker.JoinDsr(avatar=safe.address, wad=100_000_000_000_000_000_000_000)
    roles.send([join_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_balance = get_balance(w3=w3, token=ETHAddr.DAI, address=safe.address)
    assert dai_balance == 0
    pie = dsr_manager_contract.functions.pieOf(safe.address).call()
    chi = pot_contract.functions.chi().call() / (10**27)
    assert pie * chi == approx(100_000_000_000_000_000_000_000)

    # exit DAI
    exit_dai = maker.ExitDsr(avatar=safe.address, wad=50_000_000_000_000_000_000_000)
    roles.send([exit_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_balance = get_balance(w3=w3, token=ETHAddr.DAI, address=safe.address)
    assert dai_balance == approx(50_000_000_000_000_000_000_000)
    pie = dsr_manager_contract.functions.pieOf(safe.address).call()
    chi = pot_contract.functions.chi().call() / (10**27)
    assert pie * chi == approx(50_000_000_000_000_000_000_000)

    # exitAll DAI
    exit_all_dai = maker.ExitAllDsr(avatar=safe.address)
    roles.send([exit_all_dai], role=1, private_key=accounts[1].key,
                roles_mod_address=roles_ctract.address,
                web3=w3)
    dai_balance = get_balance(w3=w3, token=ETHAddr.DAI, address=safe.address)
    assert dai_balance == approx(100_000_000_000_000_000_000_000)
    pie = dsr_manager_contract.functions.pieOf(safe.address).call()
    assert pie == 0