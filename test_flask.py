from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.app_context().push()

with app.app_context():
    db.drop_all()
    db.create_all()

class UserViewsTestCase(TestCase):

    def setUp(self):
        """Adding a sample user"""
        
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
        User.query.delete()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Doug Dimmadome', html)

    def test_hompage_redirect(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)