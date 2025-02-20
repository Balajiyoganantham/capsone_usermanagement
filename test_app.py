import unittest
from appz import create_app, db
from appz.models import User
from appz.extensions import bcrypt
from base64 import b64encode

class AppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test application and database."""
        self.app = create_app()
        self.app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",  # Use in-memory DB for testing
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create a test user
            test_user = User(
                username="testuser",
                email="test@example.com",
                name="Test User",
                password=bcrypt.generate_password_hash("password").decode("utf-8"),
            )
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        """Tear down the test application and database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def get_auth_headers(self, username, password):
        """Helper function to create authorization headers."""
        credentials = b64encode(f"{username}:{password}".encode()).decode("utf-8")
        return {"Authorization": f"Basic {credentials}"}

    def test_login_success(self):
        """Test successful login."""
        response = self.client.post(
            "/login", json={"username": "testuser", "password": "password"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("Login successful", data["message"])

    def test_login_fail(self):
        """Test login failure with wrong credentials."""
        response = self.client.post(
            "/login", json={"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn("Unauthorized", data["message"])

    def test_get_users(self):
        """Test fetching users (requires authentication)."""
        headers = self.get_auth_headers("testuser", "password")
        response = self.client.get("/users", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data["users"], list)

    def test_get_user_by_id(self):
        """Test fetching a single user by ID."""
        headers = self.get_auth_headers("testuser", "password")
        response = self.client.get("/users/1", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["username"], "testuser")

    def test_unauthorized_access(self):
        """Test accessing user endpoints without authentication."""
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
