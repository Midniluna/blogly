"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

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