from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    """User"""

    def __repr__(self):
        p = self
        return f"<user id={p.id}, first_name={p.first_name}, last_name={p.last_name}, image_url={p.image_url}>"

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


