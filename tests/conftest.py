import pytest
from appz import create_app, db
from appz.models import User
from appz.extensions import bcrypt

@pytest.fixture
def app():
    """Creates and configures a new app instance for each test."""
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",  # Use in-memory DB for testing
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    with app.app_context():
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

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
