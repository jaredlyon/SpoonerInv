from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

manager = Blueprint('manager', __name__)

# Get all the employees that work for a given store and their revalent information 
@manager.route('/employee/<storeID>', methods=['GET'])
def get_employees(storeID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM `Employee` E JOIN Store S USING(store_id) WHERE E.store_id = {0};'.format(storeID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add a new employee to a given store, including their name, phone number, and email address
@manager.route('/hireEmployee', methods=['POST'])
def add_employee():
    
    the_data = request.json

    phone = the_data['phone']
    email = the_data['email']
    first_name = the_data['first_name']
    last_name = the_data['last_name']
    store_id = the_data['store_id']

    current_app.logger.info(the_data)

    # INSERT INTO Employee(phone,email,first_name,last_name,store_id) VALUES ('4088211520', 'jaredalyon@gmail.com', 'jared', 'lyon', 2);
    # "INSERT INTO Employee(phone,email,first_name,last_name,store_id) VALUES ('" + phone + "', '" + email + "', '" + first_name + "', '" + last_name + "', " + str(store_id) + ");"
    # "INSERT INTO `Employee`(phone, email, first_name, last_name, store_id) VALUES ('{phone}', '{email}', '{firstname}', '{lastname}', {storeid})".format(phone=str(phone), email=str(email), firstname=str(first_name), lastname=str(last_name), storeid=str(store_id))

    the_query = "INSERT INTO `Employee`(phone, email, first_name, last_name, store_id) VALUES ('{phone}', '{email}', '{firstname}', '{lastname}', {storeid})".format(phone=str(phone), email=str(email), firstname=str(first_name), lastname=str(last_name), storeid=str(store_id))

    current_app.logger.info(the_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()

    return "successfully hired " + first_name + " " + last_name + " at store #" + str(store_id) + " with data: " + str(the_data) + "\n and query: " + the_query

### Below is an alternate POST route that adds a new store to a region in the database
@manager.route('/addStore', methods=['POST'])
def add_store():

    the_data = request.json

    hours = the_data['hours']
    region_id = the_data['region_id']
    street = the_data['street']
    city = the_data['city']
    zip = the_data['zip']
    name = the_data['name']
    store_id = the_data['store_id']

    current_app.logger.info(the_data)

    the_query = "INSERT INTO `Store`(hours, region_id, street, city, zip, name, store_id) VALUES ('{hours}', {region_id}, '{street}', '{city}', {zip}, '{name}', {store_id})".format(hours=str(hours), region_id=str(region_id), street=str(street), city=str(city), zip=str(zip), name=str(name), store_id=str(store_id))
    
    try:
        cursor = db.get_db().cursor()
        cursor.execute(the_query)
        db.get_db().commit()
    except:
        return "query: " + the_query + "\ndb exception: failed to execute\nyou may need to reseed data since this is a primary key"

    return "successfully added " + name + " at store #" + str(store_id) + " with data: " + str(the_data) + "\n and query: " + the_query

# Update the information of a given employee, such as their name, phone number, and email address
@manager.route('/updateEmployee', methods=['PUT'])
def update_employee():
    
    the_data = request.json

    employee_id = the_data['employee_id']
    phone = the_data['phone']
    email = the_data['email']
    first_name = the_data['first_name']
    last_name = the_data['last_name']
    store_id = the_data['store_id']

    current_app.logger.info(the_data)

    the_query = 'UPDATE Employee SET '
    the_query += 'phone = "' + phone + '", '
    the_query += 'email = "' + email + '", '
    the_query += 'first_name = "' + first_name + '", '
    the_query += 'last_name = "' + last_name + '", '
    the_query += 'store_id = ' + str(store_id) + ' '
    the_query += 'WHERE employee_id = ' + str(employee_id) + ';'

    current_app.logger.info(the_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()

    return "successfully updated " + first_name + " " + last_name + " at store #" + str(store_id) + "!"

# Find and delete an employee
@manager.route('/fireEmployee/<employeeID>', methods=['DELETE'])
def delete_employee(employeeID):
    query = '''
        DELETE
        FROM Employee
        WHERE employee_id = {0};
    '''.format(employeeID)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return "successfully deleted employee #" + employeeID + "!"

# Get all the stocks available for the store to use and their revalent information
@manager.route('/stock/<storeID>', methods=['GET'])
def get_stock(storeID):
    cursor = db.get_db().cursor()
    cursor.execute('select Stock.name as name, quantity, order_date_time, Stock.stock_id as stock_id, S.store_id as store_id from Stock join Store_Stock SS on Stock.stock_id = SS.stock_id join Store S on SS.store_id = S.store_id where S.store_id = {0};'.format(storeID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update the quantity and order by date of a specified stock
@manager.route('/updateStock', methods=['PUT'])
def update_stock():
    
    the_data = request.json

    stock_id = the_data['stock_id']
    name = the_data['name']
    quantity = the_data['quantity']

    current_app.logger.info(the_data)

    # UPDATE Stock SET name = 'bingus', order_date_time = '2012-04-21T18:25:43-05:00', quantity = 254 WHERE stock_id = 2;

    the_query = 'UPDATE Stock SET '
    the_query += 'name = "' + name + '", '
    the_query += 'quantity = ' + str(quantity) + ' '
    the_query += 'WHERE stock_id = {0};'.format(stock_id)
    
    current_app.logger.info(the_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()

    return "successfully updated " + name + "!"

# Find and delete a stock item from a store
@manager.route('/deleteStock/<stockID>', methods=['DELETE'])
def delete_stock(stockID):
    query = '''
        DELETE
        FROM Stock
        WHERE stock_id = {0};
    '''.format(stockID)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return "successfully deleted stock #" + stockID + "!"

# Get all stores from a region
@manager.route('/regionalStores/<regionID>', methods=['GET'])
def get_region(regionID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from Store join Region R on Store.region_id = R.region_id where R.region_id = {0};'.format(regionID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response