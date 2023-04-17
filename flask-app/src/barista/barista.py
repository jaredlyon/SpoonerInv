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
# localhost:8001/b/Order/<orderID>
@barista.route('/Order/<orderID>', methods=['GET'])
def get_order(orderID):
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT D.drink_id as 'Drink ID', D.ice_lvl as 'Ice Level', D.price as 'Price', size as 'Size', sugar_lvl as 'Sugar Level'
                   FROM `Order` O JOIN Drink D USING(order_id) WHERE O.order_id = {0};'''.format(orderID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Returns all ingredients at the store of a given employee
@barista.route('/Ingredient/<baristaID>', methods=['GET'])
def get_ingredient(baristaID):
    query = '''
        SELECT DISTINCT I.name AS label, I.name as value
        FROM Ingredient I
        JOIN Ingredient_Recipe IR ON I.ingredient_id = IR.ingredient_id
        JOIN Stock S ON IR.stock_id = S.stock_id
        JOIN Store_Stock SS ON S.stock_id = SS.stock_id
        JOIN Store S2 ON SS.store_id = S2.store_id
        JOIN Employee E ON S2.store_id = E.store_id
        WHERE S2.store_id = {0};
    '''.format(baristaID)
    cursor = db.get_db().cursor()
    cursor.execute(query)

    json_data = []

    # fetchall the column headers and the nall the data from the cursor
    column_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchall()

    # zip headers and data togetehr into dictionaryand append to json data dict.
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)



# # TODO: Changes size, price, sugar level, and/or ice level of a drink in a given order
# @barista.route('/editDrink', methods=['PUT'])
# def edit_drink():
#     return

# Deletes a given drink
@barista.route('/DeleteDrink/<drinkID>', methods=['DELETE'])
def delete_drink(drinkID):
    query = '''
        DELETE
        FROM Drink
        WHERE drink_id = {0};
    '''.format(drinkID)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    return "success!"
    

# Deletes a given order including all of its associated drinks (assuming it cascades)
@barista.route('/DeleteOrder/<orderID>', methods=['DELETE'])
def delete_order(orderID):
    query = '''
        DELETE
        FROM `Order`
        WHERE order_id = {0};
    '''.format(orderID)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    return "success!"

# # I may have realized I fucked up the data creation for ingredients
# # I accidentally mistaken ingredients for stock
# # We should also have around five or so ingredients (since they should be unique) instead of 100

# # TODO: Updates the supply and expiration date of ingredients available
# @barista.route('/updateIngredient', methods=['PUT'])
# def update_ingredient():
#     return
