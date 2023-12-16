from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(30),
                           nullable=False)
    
    last_name = db.Column(db.String(30),
                           nullable=False)
    
    image_url = db.Column(db.String(2000),
                          default='https://t3.ftcdn.net/jpg/03/46/83/96/240_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg')

    posts = db.relationship('Post', backref='user')
    
    def __repr__(self):
        p = self
        return f"<user id={p.id}, first_name={p.first_name}, last_name={p.last_name}, image_url={p.image_url}>"

    @property
    def full_name(self):
        """Get the full name of a user"""
          
        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    """Post"""
    __tablename__="posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(30),
                      nullable=False)
    
    content = db.Column(db.String(350),
                        nullable=False)

    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))

    tags = db.relationship('Tag', 
                           secondary='posts_tags',
                           backref='posts')
    
    # user = db.relationship('User', backref='posts')
    
    def __repr__(self):
        p = self
        return f"<post id={p.id}, title={p.title}, created_at={p.created_at}>"
    
class Tag(db.Model):
    """Tag"""
    __tablename__="tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, nullable=False, unique=True)

class PostTag(db.Model):
    """Join Relationship between Post and Tag"""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"<tag id={self.id}, name={self.name}>"