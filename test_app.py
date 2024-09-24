import unittest
from app import app, db
from models import User

class UserRoutesTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up a temporary database for testing."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the database after each test."""
        with app.app_context():
            db.drop_all()

    def test_user_list(self):
        """Test GET / route (user list)."""
        with app.app_context():
            user = User(first_name="John", last_name="Doe", image_url="https://example.com/john.jpg")
            db.session.add(user)
            db.session.commit()

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"John Doe", response.data)

    def test_new_user_form(self):
        """Test GET /new-user route (show new user form)."""
        response = self.client.get("/new-user")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create a User", response.data)

    def test_add_new_user(self):
        """Test POST /new-user route (add new user)."""
        response = self.client.post("/new-user", data={
            "first_name": "Jane",
            "last_name": "Smith",
            "image_url": "https://example.com/jane.jpg"
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Jane Smith", response.data)

        # Check if user was added to the database
        with app.app_context():
            user = User.query.filter_by(first_name="Jane").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.last_name, "Smith")

    def test_user_details(self):
        """Test GET /user-details/<int:user_id> route (show user details)."""
        with app.app_context():
            user = User(first_name="John", last_name="Doe", image_url="https://example.com/john.jpg")
            db.session.add(user)
            db.session.commit()

            user_id = user.id

        response = self.client.get(f"/user-details/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"John Doe", response.data)

if __name__ == "__main__":
    unittest.main()