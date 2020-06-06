from .controller import API
from flask import jsonify


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

@API.errorhandler(500)
def api_internal_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'API internal error'
    }), 500