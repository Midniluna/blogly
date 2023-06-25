from unittest import TestCase
from flask import Flask

from app import app
from models import db, User, Post

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///blogly_test'
app.config["SQLALCHEMY_ECHO"] = False

# python test_flask.py
# python3 -m unittest test_flask.py

class UserViewsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.app_context = app.app_context()
        cls.app_context.push()

        # Create all tables in the database
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        # Remove all tables from the database and close the application context
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Adding a sample user"""

        # Clear the User table before each test
        User.query.delete()

        user = User(first_name="Doug", last_name="Dimmadome", img_url="https://pbs.twimg.com/media/Ell2E_XX0AMW0xZ.jpg")
        anon = User(first_name="Anon", last_name="Amos")
        db.session.add(user)
        db.session.add(anon)
        db.session.commit()

        self.user_id1 = user.id
        self.user1 = user
        self.user_id2 = anon.id
        self.user2 = anon

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Doug Dimmadome", html)

    def test_hompage_redirect(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)