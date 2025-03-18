// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SupplyChain {
    struct Product {
        uint id;
        string name;
        string manufacturer;
        string location;
    }

    mapping(uint => Product) public products;
    event ProductUpdated(uint id, string location);

    function addProduct(uint _id, string memory _name, string memory _manufacturer, string memory _location) public {
        require(products[_id].id == 0, "Product already exists");
        products[_id] = Product(_id, _name, _manufacturer, _location);
    }

    function updateProductLocation(uint _id, string memory _newLocation) public {
        require(products[_id].id != 0, "Product not found");
        products[_id].location = _newLocation;
        emit ProductUpdated(_id, _newLocation);
    }

    function getProduct(uint _id) public view returns (string memory name, string memory manufacturer, string memory location) {
        require(products[_id].id != 0, "Product not found");
        Product memory p = products[_id];
        return (p.name, p.manufacturer, p.location);
    }
}
