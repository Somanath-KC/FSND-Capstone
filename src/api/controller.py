from flask import Blueprint, abort, jsonify, request
from ..models import db, Article, Comment
from ..auth.handler import requires_auth

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


# GET Articles by id
# This endpoint fetches Article with given id.
@API.route('/articles/<int:article_id>', methods=["GET"])
@requires_auth('read:article')
def get_article_by_id(payload, article_id):

    articles_data = Article.query.get(article_id)

    if not articles_data:
        abort(404)

    return jsonify({
        'success': True,
        'Article': [articles_data.long()]
    })


# POST Article
# This creates new article in database
# REQUEST BODY: TYPE-> JSON
#          REQUIRED -> title, content
@API.route('/articles', methods=["POST"])
@requires_auth('post:article')
def post_article(payload):

    data = request.get_json()
    data['author'] = payload.get('sub')

    new_article = Article(**data)
    
    try:
        new_article.insert()
    except Exception as e:
        # Print statement for debugging
        print(e)
        db.session.rollback()
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
@requires_auth('update:article')
def update_article(payload):

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

    # Prevents authors from updating other author's articles
    if not payload.get('sub') == article.author:
        abort(400)

    article.content = article_new_content

    try:
        article.update()
    except Exception as e:
        #  Debugging Print Statement
        print(e)
        db.session.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'Articles': [article.long()]
    })
    

# Delete Article
# Removes an article from database with given id
# Return True if successfully deleted
@API.route('/articles/<int:article_id>', methods=["DELETE"])
@requires_auth('delete:article')
def delete_article(payload, article_id):

    article = Article.query.get(article_id)

    # Checks if article exists with given id.
    if not article:
        abort(404)
    
    # Prevents deleting others articles
    if not payload.get('sub') == article.author:
        abort(400)

    try:
        article.delete()
    except Exception as e:
        print(e)
        db.session.rollback()
        abort(422)
    
    return jsonify({
        'success': True
    })

# GET COMMENTS
# This returns all the comments for given article id
# Comment were only visible to subscribers and authors
@API.route('/articles/<int:article_id>/comments', methods=["GET"])
@requires_auth('read:comment')
def read_comments_of_article(payload, article_id):

    article = Article.query.get(article_id)

    # if passed invalid article id returns 404
    if not article:
        abort(404)

    comments = article.comments

    return jsonify({
        'success': True,
        'Article': article.title,
        'Article_id': article.id,
        'comments': [item.format() for item in comments]
    })

#  POST COMMENT
#       REQUIRES BODY --> JSON
#       BODY --> {content: "Some text"}, 
#       Returns all comments with new one.
@API.route('/articles/<int:article_id>/comments', methods=["POST"])
@requires_auth('post:comment')
def post_new_comment(payload, article_id):

    article = Article.query.get(article_id)

    # if passed invalid article id returns 404
    if not article:
        abort(404)

    comment_data = request.get_json().get('content')

    if not comment_data:
        abort(400)

    new_comment = Comment( article_id = article_id,
                           content = comment_data,
                           author = payload.get('sub') 
                         )
    
    try:
        new_comment.insert()
    except Exception as e:
        # Print Statement for debugging
        print(e)
        db.session.rollback()
        abort(422)
    
    return jsonify({
        'success': True,
        'Article': article.title,
        'Article_id': article.id,
        'comments': [item.format() for item in article.comments]
    })

    