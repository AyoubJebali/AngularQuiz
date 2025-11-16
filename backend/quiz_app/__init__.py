"""Quiz application package initialization.

This module contains the Flask application factory and extension initialization.
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .config import Config

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class=Config):
    """Create and configure the Flask application.

    Args:
        config_class: Configuration class to use (defaults to Config)

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    _init_extensions(app)

    # Register blueprints
    _register_blueprints(app)

    return app


def _init_extensions(app):
    """Initialize Flask extensions.

    Args:
        app: Flask application instance
    """
    db.init_app(app)
    login_manager.init_app(app)

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'


def _register_blueprints(app):
    """Register application blueprints.

    Args:
        app: Flask application instance
    """
    from .routes import auth, quiz

    app.register_blueprint(auth.bp)
    app.register_blueprint(quiz.bp)
