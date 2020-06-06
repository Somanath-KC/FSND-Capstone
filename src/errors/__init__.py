from flask import jsonify, request
from .. import APP



# Blueprint specific 404, 405
# Refrence: 
#       https://flask.palletsprojects.com/en/1.1.x/blueprints/#error-handlers

@APP.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404
    else:
        return error

@APP.errorhandler(405)
def method_not_allowed(error):
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404
    else:
        return error
