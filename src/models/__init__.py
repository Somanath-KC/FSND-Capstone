from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Article(db.Model):
    id = Column(Integer, primary_key=True)
    author = Column(String(), nullable=False)
    title = Column(String(), nullable=False)
    publish_date_time = Column(DateTime,  nullable=False)
    content = Column(String(),  nullable=False)

    '''
    short()
        short form representation of the Article model
    '''
    def short(self):
        
        return {
            'id': self.id,
            'title': self.title,
            'publish_date_time': self.publish_date_time
        }

    '''
    insert()
        inserts a new model into a database
        EXAMPLE
            new_article = Article(**data)
            new_article.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model into a database
        the model must exist in the database
        EXAMPLE
            article = Article.query.get(1)
            article.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            artcle = Article.query.filter(Article.id == id).one_or_none()
            article.content = 'Some Content'
            article.update()
    '''
    def update(self):
        db.session.commit()


class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, nullable=False)
    author = Column(String(), nullable=False)
    content = Column(String(256), nullable=False)
    data_time = Column(DateTime)

    '''
    insert()
        inserts a comment into a database
        EXAMPLE
            comment = Comment(**data)
            comment.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a comment from database
        the model must exist in the database
        EXAMPLE
            comment = Comment.query.get(1)
            comment.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()