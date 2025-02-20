import pytest
from appz import create_app, db
from appz.extensions import bcrypt

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    # Use an in‑memory SQLite database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

# This fixture ensures each test starts with a fresh database.
@pytest.fixture(autouse=True)
def fresh_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

@pytest.fixture
def client(app):
    return app.test_client()

# Helper function to seed a user into the test database.
def seed_user(app, username, password, email, name):
    from appz.models import User  # Import here to avoid circular imports
    with app.app_context():
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, email=email, password=hashed_password, name=name)
        db.session.add(user)
        db.session.commit()
        # Return the user's id instead of the detached instance.
        return user.id
