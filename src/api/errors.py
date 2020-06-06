from .controller import API
from flask import jsonify
from ..auth.handler import AuthError

@API.errorhandler(400)
def api_bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400

@API.errorhandler(404)
def api_resource_not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404

@API.errorhandler(405)
def api_method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method not allowed'
    }), 405

@API.errorhandler(422)
def api_method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Entity Unprocessable'
    }), 422

@API.errorhandler(500)
def api_internal_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'API internal error'
    }), 500

# Refrence: 
#          https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/#registering-an-error-handler
@API.errorhandler(AuthError)
def auth_errors(auth_error):
    error = auth_error.error
    return jsonify({
        'success': False,
        'error': error.get('error'),
        'message': error.get('message')
    }), auth_error.status_code