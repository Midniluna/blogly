"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from dotenv import dotenv_values

env_vars = dotenv_values(".env")
DB_URI = env_vars.get("DB_URI")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

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
        return f"<User id={u.id} name={u.full_name()}, url={u.img_url}>"
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=True, default = "https://st4.depositphotos.com/3864435/27060/i/1600/depositphotos_270605518-stock-photo-default-avatar-profile-icon-grey.jpg")

class Post(db.Model):

    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f'<Post #{p.id}, title={p.title}, user={p.user_id}>'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable = False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Date, nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship(User)
