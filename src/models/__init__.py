from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Article(db.Model):
    id = Column(Integer, primary_key=True)
    author = Column(String(), nullable=False)
    title = Column(String(), nullable=False)
    publish_date_time = Column(DateTime,  nullable=False)
    content = Column(String(),  nullable=False)

class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, nullable=False)
    author = Column(String(), nullable=False)
    content = Column(String(256), nullable=False)