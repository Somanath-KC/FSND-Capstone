from flask import Blueprint, abort, jsonify
from ..models import Article, Comment

API = Blueprint('API', __name__)

# API Error handling
from . import errors


# API END POINTS START

# This endpoint checks api availability
@API.route('/', methods=["GET"])
def api_index():
    return jsonify({
        'success': True
    })


# GET Articles
# This endpoint fetches all available articles
@API.route('/articles', methods=["GET"])
def get_articles():

    articles_data = [item.short() for item in Article.query.all()]


    return jsonify({
        'success': True,
        'Articles': articles_data
    })



