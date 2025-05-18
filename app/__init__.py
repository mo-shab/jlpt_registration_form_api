from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os

jwt = JWTManager()


# Load environment variables from .env
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object('app.config.Config')

    # Initialize extensions
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (add auth and other modules later)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    from app import models

    from app.routes.form_routes import form_bp
    app.register_blueprint(form_bp)

    return app
