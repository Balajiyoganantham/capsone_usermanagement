
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from appz.config import Config
from .auth import auth_bp
from .user import user_bp

from appz.db import db

# Initialize extensions
bcrypt = Bcrypt()
auth = HTTPBasicAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    from .auth import auth_bp
    from .user import user_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    return app
