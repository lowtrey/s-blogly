from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Willy", last_name="Wonka", image_url="https://picsum.photos/200")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Wonka", html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h1>{self.user.get_full_name()}</h1>", html)

    def test_add_user(self):
        with app.test_client() as client:
            test_data = {"first": "Jim", "last": "Jones", "url": "https://picsum.photos/200"}
            resp = client.post("/users/new", data=test_data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{test_data['first']} {test_data['last']}", html)

    def test_delete_user(self):
      with app.test_client() as client:
        response = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(f"{self.user.get_full_name()}", html)