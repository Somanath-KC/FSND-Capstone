from flask import Blueprint, abort, jsonify, request
from ..models import db, Article, Comment

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


# POST Article
# This creates new article in database
# REQUEST BODY: TYPE-> JSON
#          REQUIRED -> title, content
@API.route('/articles', methods=["POST"])
def post_article():

    data = request.get_json()
    data['author'] = 'somanath'

    new_article = Article(**data)
    
    try:
        new_article.insert()
    except Exception as e:
        # Print statement for debugging
        print(e)
        abort(422)

    return jsonify({
        'success': True,
        'Articles': [new_article.long()]
    }), 201 
    