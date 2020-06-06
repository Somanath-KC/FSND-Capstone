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


#  Update Article
#  This endpoint updates the existing article
#  REQUEST BODY: TYPE -> JSON
#          REQUIRED -> id, content 
@API.route('/articles', methods=['PATCH'])
def update_article():

    data = request.get_json()

    article_id = data.get('id')
    article_new_content = data.get('content')
    
    # Checks if validity  of request body 
    if not (article_id and article_new_content):
        abort(400)

    article = Article.query.get(article_id)

    #  Checks if validity of article id
    if not article:
        abort(400)

    article.content = article_new_content

    try:
        article.update()
    except Exception as e:
        #  Debugging Print Statement
        print(e)
        abort(422)

    return jsonify({
        'success': True,
        'Articles': [article.long()]
    })
    

# Delete Article
# Removes an article from database with given id
# Return True if successfully deleted
@API.route('/articles/<int:article_id>', methods=["DELETE"])
def delete_article(article_id):

    article = Article.query.get(article_id)

    # Checks if article exists with given id.
    if not article:
        abort(404)

    try:
        article.delete()
    except Exception as e:
        print(e)
        abort(422)
    
    return jsonify({
        'success': True
    })