from flask import Blueprint, request, jsonify, make_response
import json
from src import db


baristia = Blueprint('barista', __name__)