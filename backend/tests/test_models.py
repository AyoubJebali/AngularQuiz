import pytest
from quiz_app.models.models import User
from quiz_app import db
from werkzeug.security import generate_password_hash, check_password_hash

class TestUserModel:
    """Test cases for User model."""
    
    def test_user_creation(self, app):
        """Test user can be created."""
        with app.app_context():
            user = User(
                username='testuser',
                password_hash=generate_password_hash('password123')
            )
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.username == 'testuser'
            assert user.total_score == 0  # Default value
            assert check_password_hash(user.password_hash, 'password123')
    
    def test_user_unique_username(self, app):
        """Test that usernames must be unique."""
        with app.app_context():
            user1 = User(username='testuser', password_hash='hash1')
            user2 = User(username='testuser', password_hash='hash2')
            
            db.session.add(user1)
            db.session.commit()
            
            db.session.add(user2)
            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit()
    
    def test_user_default_score(self, app):
        """Test user default score is 0."""
        with app.app_context():
            user = User(username='testuser', password_hash='hash')
            assert user.total_score == 0
    
    def test_user_score_update(self, app, sample_user):
        """Test user score can be updated."""
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            original_score = user.total_score
            user.total_score += 50
            db.session.commit()
            
            updated_user = User.query.filter_by(username='testuser').first()
            assert updated_user.total_score == original_score + 50