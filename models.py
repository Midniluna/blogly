"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import datetime

# from dotenv import dotenv_values

# env_vars = dotenv_values(".env")
# DB_URI = env_vars.get("DB_URI")

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()
    

class User(db.Model):
    """User"""

    __tablename__ = "users"

    def __repr__(self):
        """Show info about the user instance"""
        u = self
        return f"<User id={u.id} name={u.full_name()}>"
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=True, default = "https://st4.depositphotos.com/3864435/27060/i/1600/depositphotos_270605518-stock-photo-default-avatar-profile-icon-grey.jpg")

    posts = db.relationship("Post", backref="users", cascade="all, delete-orphan")
    # If you add passive_deletes=True to the relationship methods, it keeps the post and leaves user_id in posts blank

class Post(db.Model):

    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f'<Post #{p.id}, title={p.title}, user={p.user_id}>'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable = False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable= False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    

class Tag(db.Model):
    __tablename__ = "tags"

    def __repr__(self):
        p = self
        return f'<Tag id={p.id}>, name={p.name}'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique = True)

    posts = db.relationship('Post', secondary='post_tag', backref='tag', cascade="all, delete")

class PostTag(db.Model):
    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
