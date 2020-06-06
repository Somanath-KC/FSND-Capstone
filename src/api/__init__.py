from flask import Blueprint, abort, jsonify

API = Blueprint('API', __name__)

# API Error handling
from . import errors

@API.route('/', methods=["GET"])
def api_index():
    return jsonify({
        'success': True
    })
