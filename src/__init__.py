import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .api.controller import API
from .models import db, Article, Comment


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    # Databse initialization
    db.app = app
    db.init_app(app)

    # CORS Configuration
    cors = CORS(app, resources={r"*": {"origin": "*"}})

    # Add CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true'
                             )
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS'
                             )
        return response

    app.register_blueprint(API, url_prefix='/api')

    @app.route('/')
    def main():
        return "E-Magazine Site."

    return app


APP = create_app()


from .errors import handler


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
