from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__= "users"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50), 
                     nullable=False,)
    
    last_name = db.Column(db.String(50), 
                     nullable=False,)
    
    image_url = db.Column(db.String,
                          nullable=True,
                          default="https://via.placeholder.com/150")
    
    posts = db.relationship("Post", backref="user")

class Post(db.Model):
    __tablename__="posts"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.Text, 
                     nullable=False,)
    
    content = db.Column(db.Text, 
                     nullable=False,)
    
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship('Tag', secondary='post_tags', backref='posts')

class Tag(db.Model):
     __tablename__="tags"

     id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
     name = db.Column(db.Text,
                     nullable=False,
                     unique=True)
     
class PostTag(db.Model):
     __tablename__="post_tags"

     post_id = db.Column(db.Integer,
                         db.ForeignKey('posts.id'),
                         primary_key=True,)
     
     tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key=True,)



def __repr__(self):
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}>"
