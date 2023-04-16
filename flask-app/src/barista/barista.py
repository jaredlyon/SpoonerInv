from flask import Blueprint, request, jsonify, make_response
import json
from src import db


barista = Blueprint('barista', __name__)