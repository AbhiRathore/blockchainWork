from flask import Flask, request, jsonify, render_template
from web3 import Web3
import json

with open("contract.json", "r") as f:
    contract_data = json.load(f)

contract_address = contract_data["address"]
abi = contract_data["abi"]

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
web3.eth.default_account = web3.eth.accounts[0]
contract = web3.eth.contract(address=contract_address, abi=abi)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.json
    product_id = int(data.get("id"))
    name = data.get("name")
    manufacturer = data.get("manufacturer")
    location = data.get("location")

    if not all([product_id, name, manufacturer, location]):
        return jsonify({"error": "All fields are required"}), 400

    tx_hash = contract.functions.addProduct(product_id, name, manufacturer, location).transact({
        "from": web3.eth.accounts[0], "gas": 500000, "gasPrice": web3.to_wei("20", "gwei")
    })
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return jsonify({"message": "Product added successfully"})

@app.route("/update_location", methods=["POST"])
def update_location():
    data = request.json
    product_id = int(data.get("id"))
    new_location = data.get("location")

    if not all([product_id, new_location]):
        return jsonify({"error": "Product ID and new location required"}), 400

    tx_hash = contract.functions.updateProductLocation(product_id, new_location).transact({
        "from": web3.eth.accounts[0], "gas": 500000, "gasPrice": web3.to_wei("20", "gwei")
    })
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return jsonify({"message": "Location updated successfully"})

@app.route("/get_product/<int:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        name, manufacturer, location = contract.functions.getProduct(product_id).call()
        return jsonify({"id": product_id, "name": name, "manufacturer": manufacturer, "location": location})
    except:
        return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
