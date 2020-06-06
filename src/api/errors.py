from . import API
from flask import jsonify

@API.errorhandler(500)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'API Internal Error'
    }), 500