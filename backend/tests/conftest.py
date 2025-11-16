import pytest
import tempfile
import os
from quiz_app import create_app, db
from quiz_app.models.models import User
from werkzeug.security import generate_password_hash
import json


@pytest.fixture
def app():
    """Create application for testing."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()

    # Create test quiz data
    test_quiz_data = [
        {
            "id": 1,
            "name": "Test Category",
            "questions": [
                {
                    "question": "What is 2+2?",
                    "options": ["3", "4", "5", "6"],
                    "correctIndex": 1,
                },
                {
                    "question": "What is the capital of France?",
                    "options": ["London", "Berlin", "Paris", "Madrid"],
                    "correctIndex": 2,
                },
            ]
            * 10,  # Duplicate to have enough questions
        }
    ]

    # Create temporary quiz file
    quiz_fd, quiz_path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(quiz_fd, "w") as f:
        json.dump(test_quiz_data, f)

    class TestConfig:
        TESTING = True
        SECRET_KEY = "test-secret-key"
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        WTF_CSRF_ENABLED = False
        QUIZ_DATA_PATH = quiz_path

    app = create_app()
    app.config.from_object(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)
    os.unlink(quiz_path)


@pytest.fixture
def client(app):
    """Test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Test runner for the Flask application."""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return auth headers."""
    # Register a test user
    client.post("/register", json={"username": "testuser", "password": "testpass123"})

    # Login to get session
    response = client.post(
        "/login", json={"username": "testuser", "password": "testpass123"}
    )

    return {"Content-Type": "application/json"}


@pytest.fixture
def sample_user(app):
    """Create a sample user in the database."""
    with app.app_context():
        user = User(
            username="testuser",
            password_hash=generate_password_hash("testpass123"),
            total_score=100,
        )
        db.session.add(user)
        db.session.commit()
        return user
