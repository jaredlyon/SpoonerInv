from flask import Blueprint, request, jsonify, make_response
import json
from src import db

# My ideas for what the front-end of this page should look like
# - Table displaying information about all the stocks used in the store
# - Form to update a given stock's supply and order by date

# These ideas I'm a little more unsure about:
# - User can specify which store they want to see all the employee information from and pull up in a table
# - From there, they can use forms to add, delete, and update employees

manager = Blueprint('manager', __name__)

# TODO: Get all the employees that work for a given store and their revalent information 
@manager.route('/employees/<storeID>', methods=['GET'])
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

# # TODO: Add a new employee to a given store, including their name, phone number, and email address
# @manager.route('/hireEmployee', methods=['POST'])
# def add_employee():
#     return

# # TODO: Update the information of a given employee, such as their name, phone number, and email address
# @manager.route('/updateEmployee', methods=['PUT'])
# def update_employee():
#     return

# TODO: Find and delete an employee
@manager.route('/fireEmployee/<employeeID>', methods=['DELETE'])
def delete_employee(employeeID):
    query = '''
        DELETE
        FROM Employee
        WHERE drink_id = {0};
    '''.format(employeeID)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    return "success!"

# TODO: Get all the stocks available for the store to use and their revalent information
@manager.route('/stock/<storeID>', methods=['GET'])
def get_stock(storeID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from Stock join Store_Stock SS on Stock.stock_id = SS.stock_id join Store S on SS.store_id = S.store_id where S.store_id = {0};'.format(storeID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# # TODO: Update the quantity and order by date of a specified stock
# @manager.route('/updateStock', methods=['PUT'])
# def update_stock():
#     return

# TODO: Get a store's information
@manager.route('/store/<storeID>', methods=['GET'])
def get_store(storeID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from Store S where S.store_id = {0};'.format(storeID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# TODO: Get all stores from a region
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