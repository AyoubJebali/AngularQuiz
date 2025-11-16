"""Main application entry point for the Quiz Flask application."""

from flask_cors import CORS

from quiz_app import create_app, db


def configure_cors(app):
    """Configure Cross-Origin Resource Sharing (CORS) for the Flask app.

    Args:
        app: Flask application instance

    Returns:
        CORS: Configured CORS instance
    """
    return CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:4200"],  # Angular dev server
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })


def initialize_database(app):
    """Initialize the database with all tables.

    Args:
        app: Flask application instance
    """
    with app.app_context():
        db.create_all()


def main():
    """Main function to run the Flask application."""
    app = create_app()

    # Configure CORS
    configure_cors(app)

    # Initialize database
    initialize_database(app)

    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()