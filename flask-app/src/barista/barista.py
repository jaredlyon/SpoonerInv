from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

# TODO: finish last update route and make order price a derived attribute from its drinks

barista = Blueprint('barista', __name__)

# Creates a new order with new drinks
# localhost:8001/b/CreateOrder
@barista.route('/createOrder', methods=['POST'])
def create_order():
    the_data = request.json

    total_price = the_data['total_price']
    store_id = the_data['store_id']
    customer_id = the_data['customer_id']

    current_app.logger.info(the_data)

    the_query = 'INSERT INTO `Order`(total_price, store_id, customer_id) VALUES ('
    the_query += str(total_price) + ', '
    the_query += str(store_id) + ', '
    the_query += str(customer_id) + ')'

    current_app.logger.info(the_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()

    return "success!"

# Creates a new drink within a given order
# localhost:8001/b/CreateDrink
@barista.route('/createDrink', methods=['POST', 'PUT'])
def create_drink():

    the_data = request.json

    size = the_data['size']
    sugar_lvl = the_data['sugar_lvl']
    ice_lvl = the_data['ice_lvl']
    price = the_data['price']
    order_id = the_data['order_id']

    current_app.logger.info(the_data)

    the_query = 'INSERT INTO Drink(size,sugar_lvl,ice_lvl,price,order_id) VALUES ("'
    the_query += size + '", "'
    the_query += sugar_lvl + '", "'
    the_query += ice_lvl + '", '
    the_query += str(price) + ', '
    the_query += str(order_id) + ')'

    current_app.logger.info(the_query)

    # update the total price of the order
    order_query = 'UPDATE `Order` SET total_price = total_price + ' + str(price) + ' WHERE order_id = ' + str(order_id) + ';'

    current_app.logger.info(order_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    cursor.execute(order_query)
    db.get_db().commit()

    return "success!"

# Gets all of the drinks associated with an order
# localhost:8001/b/Order/<orderID>
@barista.route('/order/<orderID>', methods=['GET'])
def get_order(orderID):
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT D.drink_id as 'DrinkID', D.ice_lvl as 'IceLevel', D.price as 'Price', size as 'Size', sugar_lvl as 'SugarLevel'
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
# localhost:8001/b/Ingredient/<baristaID>
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



# Changes size, price, sugar level, and/or ice level of a drink in a given order
# localhost:8001/b/EditDrink/<drinkID>
@barista.route('/editDrink/<drinkID>', methods=['PUT'])
def update_drink(drinkID):
    
    the_data = request.json

    size = the_data['size']
    sugar_lvl = the_data['sugar_lvl']
    ice_lvl = the_data['ice_lvl']
    price = the_data['price']
    order_id = the_data['order_id']

    current_app.logger.info(the_data)

    the_query = 'UPDATE Drink SET '
    the_query += 'size = "' + size + '", '
    the_query += 'sugar_lvl = "' + sugar_lvl + '", '
    the_query += 'ice_lvl = "' + ice_lvl + '", '
    the_query += 'price = ' + str(price) + ', '
    the_query += 'order_id =' + str(order_id) + ' '
    the_query += 'WHERE drink_id = {0};'.format(drinkID)

    current_app.logger.info(the_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()

    return "success!"

# Deletes a given drink
# localhost:8001/b/DeleteDrink/<drinkID>
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
# localhost:8001/b/DeleteOrder/<orderID>
@barista.route('/deleteOrder/<orderID>', methods=['DELETE'])
def delete_order(orderID):
    query = '''
        DELETE
        FROM `Order`
        WHERE order_id = {0};
    '''.format(orderID)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    return "success!"

# # TODO: Updates the supply and expiration date of ingredients available
# @barista.route('/updateIngredient', methods=['PUT'])
# def update_ingredient():
#     return

# Gets the count of distinct orders from the database
# Returns the count as an integer
@barista.route('/order', methods=['GET'])
def get_next_order():
    query = '''
        SELECT MAX(order_id) as next_id
        FROM `Order`;
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    json_data = []

    # fetchall the column headers and the nall the data from the cursor
    column_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchall()

    # zip headers and data together into dictionaryand append to json data dict.
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    jsonify(json_data)

    return str(json_data[0]['next_id'])

# Gets the store ID of a given employee
@barista.route('/employeeStore/<employeeID>', methods=['GET'])
def get_employee_store(employeeID):
    query = '''SELECT Store.store_id as store_id from Store join Employee E on Store.store_id = E.store_id where E.employee_id = {0};'''.format(employeeID)
        
    cursor = db.get_db().cursor()
    cursor.execute(query)

    json_data = []

    # fetchall the column headers and the nall the data from the cursor
    column_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchall()

    # zip headers and data togetehr into dictionaryand append to json data dict.
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    jsonify(json_data)

    return str(json_data[0]['store_id'])