
import flask
if not hasattr(flask, '_request_ctx_stack'):
    flask._request_ctx_stack = flask._app_ctx_stack

import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from appz import create_app, db
from appz.extensions import bcrypt

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(autouse=True)
def fresh_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

@pytest.fixture
def client(app):
    return app.test_client()


def seed_user(app, username, password, email, name):
    from appz.models import User 
    with app.app_context():
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, email=email, password=hashed_password, name=name)
        db.session.add(user)
        db.session.commit()
        return user.id
