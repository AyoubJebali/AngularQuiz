"""Helper functions for testing the quiz application."""

import json
from werkzeug.security import generate_password_hash
from quiz_app.models.models import User
from quiz_app import db


def create_test_user(username="testuser", password="testpass123", score=0):
    """Create a test user in the database.
    
    Args:
        username (str): Username for the test user
        password (str): Password for the test user
        score (int): Initial score for the test user
        
    Returns:
        User: The created user object
    """
    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        total_score=score
    )
    db.session.add(user)
    db.session.commit()
    return user


def create_multiple_test_users(user_data):
    """Create multiple test users from a list of user data.
    
    Args:
        user_data (list): List of dicts with keys: username, password, score
        
    Returns:
        list: List of created User objects
    """
    users = []
    for data in user_data:
        user = create_test_user(
            username=data['username'],
            password=data['password'],
            score=data.get('score', 0)
        )
        users.append(user)
    return users


def assert_valid_quiz_response(response_data):
    """Assert that a quiz response has the correct structure.
    
    Args:
        response_data (list): The quiz response data to validate
    """
    assert isinstance(response_data, list), "Quiz response should be a list"
    assert len(response_data) > 0, "Quiz response should not be empty"
    
    for question in response_data:
        assert 'question' in question, "Question should have 'question' field"
        assert 'options' in question, "Question should have 'options' field"
        assert 'correctIndex' in question, "Question should have 'correctIndex' field"
        assert isinstance(question['options'], list), "Options should be a list"
        assert len(question['options']) >= 2, "Should have at least 2 options"
        assert isinstance(question['correctIndex'], int), "correctIndex should be an integer"
        assert 0 <= question['correctIndex'] < len(question['options']), "correctIndex should be valid"


def assert_valid_user_response(response_data, expected_username=None):
    """Assert that a user response has the correct structure.
    
    Args:
        response_data (dict): The user response data to validate
        expected_username (str, optional): Expected username to verify
    """
    assert isinstance(response_data, dict), "User response should be a dict"
    assert 'username' in response_data, "User response should have 'username' field"
    
    if expected_username:
        assert response_data['username'] == expected_username, f"Expected username {expected_username}"


def mock_quiz_data(num_questions=10, category_id=1, category_name="Test Category"):
    """Generate mock quiz data for testing.
    
    Args:
        num_questions (int): Number of questions to generate
        category_id (int): ID for the category
        category_name (str): Name for the category
        
    Returns:
        list: Mock quiz data structure
    """
    questions = []
    for i in range(num_questions):
        questions.append({
            "question": f"Test question {i + 1}?",
            "options": [f"Option A{i}", f"Option B{i}", f"Option C{i}", f"Option D{i}"],
            "correctIndex": i % 4  # Rotate through options
        })
    
    return [{
        "id": category_id,
        "name": category_name,
        "questions": questions
    }]


def clean_database():
    """Clean all data from the test database."""
    User.query.delete()
    db.session.commit()
