from flask import Blueprint, request, jsonify, make_response
import json
from src import db

# My ideas for what the front-end of this page should look like
# - Table displaying information about all the ingredients used in the store
# - Form to update a given ingredient's supply and expiration date
# - Separate forms to delete and add orders

# These ideas I'm a little more unsure about:
# - User can specify what order they want to see and pull up all the drinks in that order in a table
# - From there, they can use forms to add, delete, and update drinks

barista = Blueprint('barista', __name__)

# # TODO: Creates a new order with new drinks
# # Must specify customer name, store name, and all drinks associated
# @barista.route('/createOrder', methods=['POST'])
# def create_order():
#     return

# # TODO: Creates a new drink within a given order
# # Must specify size, price, sugar level, ice level, and maybe order ID
# @barista.route('/createDrink', methods=['POST'])
# def create_drink():
#     return

# Gets all of the drinks associated with an order
# localhost:8001/b/order/<orderID>
@barista.route('/order/<orderID>', methods=['GET'])
def get_order(orderID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM `Order` O JOIN Drink D USING(order_id) WHERE O.order_id = {0};'.format(orderID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# # TODO: Returns all ingredients
# @barista.route('/Ingredient', methods=['GET'])
# def get_ingredient():
#     return

# # TODO: Changes size, price, sugar level, and/or ice level of a drink in a given order
# @barista.route('/editDrink', methods=['PUT'])
# def edit_drink():
#     return

# # TODO: Deletes a given drink from a given order
# @barista.route('/deleteDrink', method=['DELETE'])
# def delete_drink():
#     return

# # TODO: Deletes a given order including all of its associated drinks (assuming it cascades)
# @barista.route('/deleteOrder', methods=['DELETE'])
# def delete_order():
#     return

# # I may have realized I fucked up the data creation for ingredients
# # I accidentally mistaken ingredients for stock
# # We should also have around five or so ingredients (since they should be unique) instead of 100

# # TODO: Updates the supply and expiration date of ingredients available
# @barista.route('/updateIngredient', methods=['PUT'])
# def update_ingredient():
#     return

# # TODO: Gets all of the ingredients used in the shop and any other revalent information
# @barista.route('/ingredients', methods=['GET'])
# def get_ingredients():
#     return