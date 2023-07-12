import json
from roles_royce.utils import MULTISENDS
from roles_royce.evm_utils import roles_abi, roles_bytecode
from roles_royce import Chain

from .utils import TEST_ACCOUNTS, safe_send


def deploy_roles(w3, avatar):
    # Deploy a Roles contrat without using the ProxyFactory (to simplify things)
    role_constructor_bytes = "000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001"
    bytecode_without_default_constructor = roles_bytecode[:-len(role_constructor_bytes)]

    ctract = w3.eth.contract(abi=roles_abi, bytecode=bytecode_without_default_constructor)

    owner = avatar = target = w3.to_checksum_address(avatar)
    tx_receipt = ctract.constructor(owner, avatar, target).transact({"from": avatar})  # deploy!
    roles_ctract_address = w3.eth.get_transaction_receipt(tx_receipt).contractAddress

    ctract = w3.eth.contract(roles_ctract_address, abi=roles_abi)
    ctract.functions.setMultisend(MULTISENDS[Chain.ETHEREUM]).transact({"from": avatar})
    return ctract

def setup_common_roles(safe, roles_ctract):
    # set roles_mod as module of safe
    enable_module_roles = safe.contract.functions.enableModule(roles_ctract.address).build_transaction({"from": safe.address})['data']
    safe_send(safe, to=safe.address, data=enable_module_roles, signer_key=TEST_ACCOUNTS[0].key)

    # enable an asign roles to the test EOAs
    # EOA           | ROLE N | ROLE NAME
    # accounts[1]   |  1     | Manager
    # accounts[2]   |  2     | revoker
    # accounts[3]   |  3     | harvester
    # accounts[4]   |  4     | disassembler
    # accounts[5]   |  5     | swapper

    for role_number in range(1, 6):
        account = TEST_ACCOUNTS[role_number]
        enable_module = roles_ctract.functions.enableModule(account.address).build_transaction({"from": safe.address})['data']
        safe_send(safe, to=roles_ctract.address, data=enable_module, signer_key=TEST_ACCOUNTS[0].key)

        assign_role = roles_ctract.functions.assignRoles(account.address, [role_number], [True]).build_transaction({"from": safe.address})['data']
        safe_send(safe, to=roles_ctract.address, data=assign_role, signer_key=TEST_ACCOUNTS[0].key)

def apply_presets(safe, roles_ctract, json_data, signer_key, replaces=None):
    presets_data = json.loads(json_data)
    for tx in presets_data["transactions"]:
        data: str = tx['data']
        for replacer in replaces:
            data = data.replace(replacer[0], replacer[1])
        safe_send(safe, to=roles_ctract.address, data=data, signer_key=signer_key)

