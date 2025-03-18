from web3 import Web3
import json
import solcx

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
web3.eth.default_account = web3.eth.accounts[0]


# set_solc_version("0.8.20")
def compile_source_file(file_path):
    solcx.install_solc(version='0.8.9')
    solcx.set_solc_version('0.8.9')
    with open(file_path, 'r') as f:
        source = f.read()
        print(source)
    return solcx.compile_source(source)

# with open("SupplyChain.sol", "r") as file:
#     contract_source = file.read()

compiled_sol = compile_source_file("supplychain.sol")
contract_interface = compiled_sol["<stdin>:SupplyChain"]

SupplyChain = web3.eth.contract(abi=contract_interface["abi"], bytecode=contract_interface["bin"])
tx_hash = SupplyChain.constructor().transact()
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress
abi = contract_interface["abi"]

print(f"Contract deployed at {contract_address}")

with open("contract.json", "w") as f:
    json.dump({"address": contract_address, "abi": abi}, f)
