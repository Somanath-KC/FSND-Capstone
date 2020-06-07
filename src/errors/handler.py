from flask import jsonify, request
from .. import APP
from ..api.errors import api_resource_not_found, api_method_not_allowed


# Blueprint specific 404, 405 error handling
# Refrence:
# https://flask.palletsprojects.com/en/1.1.x/blueprints/#error-handlers
@APP.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        print("its api")
        return api_resource_not_found(error)
    else:
        return error


@APP.errorhandler(405)
def method_not_allowed(error):
    if request.path.startswith('/api/'):
        return api_method_not_allowed(error)
    else:
        return error
