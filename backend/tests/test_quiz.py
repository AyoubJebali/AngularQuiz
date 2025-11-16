import json
import pytest
from unittest.mock import patch, mock_open
from quiz_app.models.models import User
from quiz_app import db

class TestQuizRoutes:
    """Test cases for quiz routes."""
    
    def test_get_quizzes_success(self, client):
        """Test successful quiz retrieval."""
        response = client.get('/quizzes?category_ids=1')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 10  # Should return 10 questions
        
        # Check question structure
        if data:
            question = data[0]
            assert 'question' in question
            assert 'options' in question
            assert 'correctIndex' in question
            assert isinstance(question['options'], list)
            assert len(question['options']) >= 2
    
    def test_get_quizzes_missing_category_ids(self, client):
        """Test quiz retrieval without category IDs."""
        response = client.get('/quizzes')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Category IDs are required' in data['error']
    
    def test_get_quizzes_invalid_category_ids(self, client):
        """Test quiz retrieval with invalid category IDs."""
        response = client.get('/quizzes?category_ids=999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'No categories found' in data['error']
    
    def test_get_quizzes_multiple_categories(self, client):
        """Test quiz retrieval with multiple category IDs."""
        response = client.get('/quizzes?category_ids=1,2')
        
        # Should handle gracefully even if category 2 doesn't exist
        assert response.status_code in [200, 404]
    
    def test_get_leaderboard_empty(self, client):
        """Test leaderboard when no users exist."""
        response = client.get('/leaderboard')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_leaderboard_with_users(self, client, app):
        """Test leaderboard with users."""
        with app.app_context():
            # Create test users with different scores
            users = [
                User(username='user1', password_hash='hash1', total_score=100),
                User(username='user2', password_hash='hash2', total_score=200),
                User(username='user3', password_hash='hash3', total_score=150),
            ]
            for user in users:
                db.session.add(user)
            db.session.commit()
        
        response = client.get('/leaderboard')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 3
        
        # Check if sorted by score (descending)
        assert data[0]['score'] == 200
        assert data[1]['score'] == 150
        assert data[2]['score'] == 100
        assert data[0]['username'] == 'user2'
    
    def test_save_score_success(self, client, app):
        """Test successful score saving."""
        with app.app_context():
            user = User(username='testuser', password_hash='hash', total_score=50)
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/saveScore', json={
            'username': 'testuser',
            'score': 25
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Score saved successfully'
        
        # Verify score was updated
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            assert user.total_score == 75  # 50 + 25
    
    

    @patch('quiz_app.routes.quiz.load_quiz_data')
    def test_quiz_file_not_found(self, mock_load, client):
        """Test behavior when quiz file is not found."""
        mock_load.return_value = []
        
        response = client.get('/quizzes?category_ids=1')
        assert response.status_code == 404