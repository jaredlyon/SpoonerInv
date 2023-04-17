from flask import Blueprint, request, jsonify, make_response
import json
from src import db

# My ideas for what the front-end of this page should look like
# - Table displaying information about all the ingredients used in the store
# - Form to update a given ingredient's supply and expiration date
# - Separate forms to delete and add orders
# - 

barista = Blueprint('barista', __name__)

# TODO: Creates a new order with new drinks
# Must specify customer name, store name, and all drinks associated
@barista.route('/createOrder', methods=['POST'])
def create_order():
    return

# TODO: Creates a new drink within a given order
# Must specify size, price, sugar level, ice level, and maybe order ID
@barista.route('/createDrink', methods=['POST'])
def create_drink():
    return

# TODO: Gets all of the drinks associated with an order
@barista.route('/order', methods=['GET'])
def get_order():
    return

# TODO: Changes size, price, sugar level, and/or ice level of a drink in a given order
@barista.route('/editDrink', methods=['PUT'])
def edit_drink():
    return

# TODO: Deletes a given drink from a given order
@barista.route('/deleteDrink', method=['DELETE'])
def delete_drink():
    return

# TODO: Deletes a given order including all of its associated drinks (assuming it cascades)
@barista.route('/deleteOrder', methods=['DELETE'])
def delete_order():
    return

# I may have realized I fucked up the data creation for ingredients
# I accidentally mistaken ingredients for stock
# We should also have around five or so ingredients (since they should be unique) instead of 100

# TODO: Updates the supply and expiration date of ingredients available
@barista.route('/updateIngredient', methods=['PUT'])
def update_ingredient():
    return

# TODO: Gets all of the ingredients used in the shop and any other revalent information
@barista.route('/ingredient', methods=['GET'])
def get_ingredient():
    return