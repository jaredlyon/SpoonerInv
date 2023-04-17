from flask import Blueprint, request, jsonify, make_response
import json
from src import db


manager = Blueprint('manager', __name__)

# TODO: Get all the employees that work for a given store and their revalent information 
@manager.route('/employees', methods=['GET'])
def get_employees():
    return

# TODO: Add a new employee to a given store, including their name, phone number, and email address
@manager.route('/hireEmployee', methods=['POST'])
def add_employee():
    return

# TODO: Update the information of a given employee, such as their name, phone number, and email address
@manager.route('/updateEmployee', methods=['PUT'])
def update_employee():
    return

# TODO: Find and delete an employee
@manager.route('/fireEmployee', methods=['DELETE'])
def delete_employee():
    return

# TODO: Get all the stocks available for the store to use and their revalent information
@manager.route('/stocks', methods=['GET'])
def get_stocks():
    return

# TODO: Update the quantity and order by date of a specified stock
@manager.route('/updateStock', methods=['PUT'])
def update_stock():
    return

