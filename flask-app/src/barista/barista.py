from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

barista = Blueprint('barista', __name__)

# Creates a new order (with no drinks)
@barista.route('/createOrder', methods=['POST'])
def create_order():
    the_data = request.json

    employee_id = the_data['employee_id']
    customer_id = the_data['customer_id']

    current_app.logger.info(the_data)
    
    # get the store_id of the employee
    store_id = get_employee_store(employee_id)

    the_query = 'INSERT INTO `Order`(total_price, store_id, customer_id) VALUES ('
    the_query += str(0) + ', '
    the_query += str(store_id) + ', '
    the_query += str(customer_id) + ')'

    current_app.logger.info(the_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()

    # get the "next" order number (the one for this order that you just added)
    current_order = get_next_order()
    return current_order

# Creates a new drink within a given order
# Also updates the corresponding order's total price!!
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

    return "successfully created drink and added to order #{0}!".format(order_id)

# Gets all of the drinks associated with an order
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
        
    return jsonify(json_data)


# Returns all ingredients at the store of a given employee
@barista.route('/ingredient/<baristaID>', methods=['GET'])
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
@barista.route('/editDrink/<drinkID>', methods=['PUT'])
def update_drink(drinkID):
    
    the_data = request.json

    size = the_data['Size']
    sugar_lvl = the_data['SugarLevel']
    ice_lvl = the_data['IceLevel']
    price = the_data['Price']
    
    # grab order_id and previous drink price for the given drink
    drinkInfo = get_drink_info(drinkID)
    
    orderID = str(drinkInfo['order_id'])
    prev_price = str(drinkInfo['price'])
    
    # calculate price change (if any)
    price_change = float(price) - float(prev_price)
    
    # update order total price
    order_query = 'UPDATE `Order` SET total_price = total_price + ' + str(price_change) + ' WHERE order_id = ' + str(orderID) + ';'

    current_app.logger.info(the_data)

    the_query = 'UPDATE Drink SET '
    the_query += 'size = "' + size + '", '
    the_query += 'sugar_lvl = "' + sugar_lvl + '", '
    the_query += 'ice_lvl = "' + ice_lvl + '", '
    the_query += 'price = ' + str(price) + ' '
    the_query += 'WHERE drink_id = {0};'.format(drinkID)

    current_app.logger.info(the_query)
    
    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    cursor.execute(order_query)
    db.get_db().commit()

    return "successfully editted drink #{0}!".format(drinkID)

# Edit information of an order
@barista.route('/editOrder', methods=['PUT'])
def update_order():
    the_data = request.json

    order_id = the_data["Edit_Order_Id"]
    customer_id = the_data['Edit_Order_Cust_Id']
    total_price = the_data['Edit_Order_Total_Price']

    current_app.logger.info(the_data)

    the_query = 'Update `Order` SET '
    the_query += 'customer_id = ' + str(customer_id) + ', '
    the_query += 'total_price = ' + str(total_price) + ' '
    the_query += 'WHERE order_id = ' + order_id + ';'

    current_app.logger.info(the_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()

    return "successfully editted order #{0}!".format(order_id)

# Deletes a given drink
# Also reduces the corresponding order's total price
@barista.route('/deleteDrink/<drinkID>', methods=['DELETE'])
def delete_drink(drinkID):
    query = '''
        DELETE
        FROM Drink
        WHERE drink_id = {0};
    '''.format(drinkID)
    
    # grab order_id and previous drink price for the given drink
    drinkInfo = get_drink_info(drinkID)
    
    orderID = str(drinkInfo['order_id'])
    price = str(drinkInfo['price'])
    
    # update order total price
    order_query = 'UPDATE `Order` SET total_price = total_price - ' + str(price) + ' WHERE order_id = ' + str(orderID) + ';'
    
    cursor = db.get_db().cursor()
    cursor.execute(order_query)
    cursor.execute(query)
    
    db.get_db().commit()
    return "successfully deleted drink #{0}!".format(drinkID)

# Deletes a given order including all of its associated drinks (assuming it cascades)
@barista.route('/deleteOrder/<orderID>', methods=['DELETE'])
def delete_order(orderID):
    query = '''
        DELETE
        FROM `Order`
        WHERE order_id = {0};
    '''.format(orderID)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    db.get_db().commit()
    return "successfully deleted order #{0}!".format(orderID)

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

    # fetch all the column headers and the nall the data from the cursor
    column_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchall()

    # zip headers and data together into dictionary and append to json data dict.
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

    # zip headers and data together into dictionary and append to json data dict.
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    jsonify(json_data)

    return str(json_data[0]['store_id'])

# Get a customer id from a given order id
@barista.route('/orderCust/<orderID>', methods=['GET'])
def get_order_custid(orderID):
    query = '''SELECT * FROM `Order` WHERE order_id = {0};'''.format(orderID)

    cursor = db.get_db().cursor()
    cursor.execute(query)

    json_data = []
    column_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchall()

    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    
    jsonify(json_data)
    
    # return first row of json data and grab customer_id column
    return str(json_data[0]['customer_id'])

# Get a customer id from a given order id
@barista.route('/orderPrice/<orderID>', methods=['GET'])
def get_order_total_price(orderID):
    query = '''SELECT * FROM `Order` WHERE order_id = {0};'''.format(orderID)

    cursor = db.get_db().cursor()
    cursor.execute(query)

    json_data = []
    column_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchall()

    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    
    jsonify(json_data)

    # return first row of json data and grab total_price column
    return str(json_data[0]['total_price'])

# Get the order_id and price of a drink
@barista.route('/drinkInfo/<drinkID>', methods=['GET'])
def get_drink_info(drinkID):
    query = '''SELECT O.order_id, D.price
                FROM Drink D
                JOIN `Order` O USING(order_id)
                WHERE D.drink_id = {0};'''.format(drinkID)

    cursor = db.get_db().cursor()
    cursor.execute(query)

    json_data = []
    column_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchall()

    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    jsonify(json_data)

    return json_data[0]
    #return str(json_data[0]['price'])