from flask import Flask
from .config import Config
from .db import db
from .extensions import bcrypt, auth  # Import shared instances

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)  # Initialize bcrypt

    from .routes.auth import auth_bp
    from .routes.user import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    return app
