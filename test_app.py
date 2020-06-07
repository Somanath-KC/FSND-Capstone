import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from src import APP
from src.models import Article, Comment

author1_jwt = os.environ.get('AUTHOR1_JWT')
subscriber_jwt = os.environ.get('SUBSCRIBER_JWT')


class EmagazineAPITestCase(unittest.TestCase):
    """This class represents the emagazine test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_articles(self):
        res = self.client().get('/api/articles')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('Articles'))

    def test_api_invalid_endpoint(self):
        res = self.client().get('/api/fasdl')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)

    def test_get_article_by_id_with_auth(self):
        # Using subscriber jwt for RBAC testing
        headers = {"Authorization": "Bearer {}".format(subscriber_jwt)}
        res = self.client().get('/api/articles/3', headers=headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('Article'))

    def test_get_article_by_id_without_auth(self):
        # RBAC testing without auth header
        # Only Subscribers can read the articles
        res = self.client().get('/api/articles/3')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('success'), False)
        self.assertFalse(data.get('Article'))

    def test_get_articles_by_wrong_id(self):
        # Using subscriber jwt for RBAC testing
        headers = {"Authorization": "Bearer {}".format(subscriber_jwt)}
        res = self.client().get('/api/articles/453', headers=headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)
        self.assertFalse(data.get('Articles'))

    def test_post_new_article_by_author(self):
        # Using author's jwt for testing
        # Only authors can post articles in magazine
        headers = {"Authorization": "Bearer {}".format(author1_jwt)}
        content = {"title": "Test Title", 
                   "content": "Content of Article goes here."
                   }
        res = self.client().post('/api/articles', headers=headers, json=content)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('Articles'))

    def test_post_new_article_by_subscriber(self):
        # Using subscirber's jwt for RBAC testing
        # Only authors can post articles in magazine but not subscriber
        headers = {"Authorization": "Bearer {}".format(subscriber_jwt)}
        content = {"title": "Test Title",
                   "content": "Content of Article goes here."
                   }
        res = self.client().post('/api/articles', headers=headers, json=content)
        data = res.get_json()

        self.assertTrue(res.status_code, 401)
        self.assertFalse(data.get('success'))
        self.assertFalse(data.get('Articles'))

    def test_update_article_by_author(self):
        # Using author's jwt for RBAC testing
        # Only authors can update articles in magazine
        headers = {"Authorization": "Bearer {}".format(author1_jwt)}
        content = {"id": 10, "content": "Content of Article goes here."}
        res = self.client().patch('/api/articles', headers=headers, json=content)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('Articles'))

    def test_update_article_by_author_invalid_body(self):
        # Using author's jwt for RBAC testing
        # Only authors can update articles in magazine
        # Intentionally missed id from body
        headers = {"Authorization": "Bearer {}".format(author1_jwt)}
        content = {"content": "Content of Article goes here."}
        res = self.client().patch('/api/articles', headers=headers, json=content)
        data = res.get_json()

        self.assertTrue(res.status_code, 400)
        self.assertFalse(data.get('success'))

    def test_delete_article_by_author(self):
        # Using author's jwt for RBAC testing
        # Only authors can delete there own articles in magazine

        # For testing purpose here we are inserting a new article
        # Which will be deleted during the test
        post_headers = {"Authorization": "Bearer {}".format(author1_jwt)}
        post_content = {"title": "Test Title", "content": "Content of Article goes here."}
        post_res = self.client().post('/api/articles', headers=post_headers, json=post_content)
        post_data = post_res.get_json()

        article_id = post_data.get('Articles')[0].get('id')
        headers = {"Authorization": "Bearer {}".format(author1_jwt)}
        res = self.client().delete('/api/articles/{}'.format(article_id), headers=headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))

    def test_delete_article_by_subscriber(self):
        # Using author's jwt for RBAC testing
        # Only authors can delete there own articles in magazine

        # For testing purpose here we are inserting a new article
        # Which will be deleted during the test
        post_headers = {"Authorization": "Bearer {}".format(author1_jwt)}
        post_content = {"title": "Test Title", "content": "Content of Article goes here."}
        post_res = self.client().post('/api/articles', headers=post_headers, json=post_content)
        post_data = post_res.get_json()

        # Here we are using subscriber jwt to delete article which will eventually fail
        article_id = post_data.get('Articles')[0].get('id')
        headers = {"Authorization": "Bearer {}".format(subscriber_jwt)}
        res = self.client().delete('/api/articles/{}'.format(article_id), headers=headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data.get('success'))

    def test_get_comments_by_public(self):
        # Comments can only read by sucscribers not by public
        article_id = 3
        res = self.client().get('/api/articles/{}/comments'.format(article_id))
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data.get('success'))

    def test_get_comments_by_subscriber(self):
        article_id = 3
        headers = {"Authorization": "Bearer {}".format(subscriber_jwt)}
        res = self.client().get('/api/articles/{}/comments'.format(article_id), headers=headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('Article_id'), article_id)
        self.assertTrue(data.get('comments'))

    def test_post_comment_by_subscriber(self):
        # For testing purpose here we are inserting a new article
        # Which will be used for commenting
        post_headers = {"Authorization": "Bearer {}".format(author1_jwt)}
        post_content = {"title": "Test Title", "content": "Content of Article goes here."}
        post_res = self.client().post('/api/articles',
                                      headers=post_headers,
                                      json=post_content
                                      )
        post_data = post_res.get_json()

        article_id = post_data.get('Articles')[0].get('id')
        headers = {"Authorization": "Bearer {}".format(author1_jwt)}
        content = {"content": "This is a testing comment"}
        res = self.client().post('/api/articles/{}/comments'.format(article_id),
                                 headers=headers,
                                 json=content
                                 )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))

    def test_post_comment_by_public(self):
        # For testing purpose here we are inserting a new article
        # Which will be used for commenting
        post_headers = {"Authorization": "Bearer {}".format(author1_jwt)}
        post_content = {"title": "Test Title", "content": "Content of Article goes here."}
        post_res = self.client().post('/api/articles', headers=post_headers, json=post_content)
        post_data = post_res.get_json()

        # Here no auth is used, hence this request
        # will be treated as public request
        article_id = post_data.get('Articles')[0].get('id')
        content = {"content": "This is a testing comment"}
        res = self.client().post('/api/articles/{}/comments'.format(article_id), json=content)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data.get('success'))

    def test_delete_comment_by_subscriber(self):
        # For testing purpose here we are inserting a new article
        # Which will be used for commenting
        post_headers = {"Authorization": "Bearer {}".format(author1_jwt)}
        post_content = {"title": "Test Title", "content": "Content of Article goes here."}
        post_res = self.client().post('/api/articles', headers=post_headers, json=post_content)
        post_data = post_res.get_json()

        # Using subscriber jwt for auth
        article_id = post_data.get('Articles')[0].get('id')
        headers = {"Authorization": "Bearer {}".format(subscriber_jwt)}
        content = {"content": "This is a testing comment"}
        res = self.client().post('/api/articles/{}/comments'.format(article_id),
                                 headers=headers,
                                 json=content
                                 )
        data = res.get_json()

        # Get the id of last inserted comment and delete it
        comment_id = data.get('comments')[-1].get('id')
        comment_id_content = {"id": comment_id}
        delete_req = self.client().delete('/api/articles/{}/comments'.format(article_id),
                                          headers=headers,
                                          json=comment_id_content
                                          )
        delete_data = delete_req.get_json()

        self.assertEqual(delete_req.status_code, 200)
        self.assertTrue(delete_data.get('success'))

    def test_delete_comment_by_public(self):
        # For testing purpose here we are inserting a new article
        # Which will be used for commenting
        post_headers = {"Authorization": "Bearer {}".format(author1_jwt)}
        post_content = {"title": "Test Title", "content": "Content of Article goes here."}
        post_res = self.client().post('/api/articles',
                                      headers=post_headers,
                                      json=post_content
                                      )
        post_data = post_res.get_json()

        # Using subscriber jwt for auth
        article_id = post_data.get('Articles')[0].get('id')
        headers = {"Authorization": "Bearer {}".format(subscriber_jwt)}
        content = {"content": "This is a testing comment"}
        res = self.client().post('/api/articles/{}/comments'.format(article_id),
                                 headers=headers,
                                 json=content
                                 )
        data = res.get_json()

        # Get the id of last inserted comment and delete it
        comment_id = data.get('comments')[-1].get('id')
        comment_id_content = {"id": comment_id}
        # No auth header is provied
        delete_req = self.client().delete('/api/articles/{}/comments'.format(article_id),
                                          json=comment_id_content
                                          )
        delete_data = delete_req.get_json()

        self.assertEqual(delete_req.status_code, 401)
        self.assertFalse(delete_data.get('success'))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
