import json
import pytest
from quiz_app.models.models import User
from quiz_app import db

class TestAuthRoutes:
    """Test cases for authentication routes."""
    
    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post('/register', json={
            'username': 'newuser',
            'password': 'password123'
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'User created successfully'
    
    def test_register_duplicate_username(self, client):
        """Test registration with existing username fails."""
        # Register first user
        client.post('/register', json={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Try to register with same username
        response = client.post('/register', json={
            'username': 'testuser',
            'password': 'differentpass'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Username already exists' in data['error']
    
    def test_register_missing_data(self, client):
        """Test registration with missing data."""
        response = client.post('/register', json={
            'username': 'testuser'
            # Missing password
        })
        
        assert response.status_code in [400, 500]  # Should handle gracefully
    
    def test_login_success(self, client):
        """Test successful login."""
        # Register user first
        client.post('/register', json={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Login
        response = client.post('/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['username'] == 'testuser'
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post('/login', json={
            'username': 'nonexistent',
            'password': 'wrongpass'
        })
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid credentials' in data['error']
    
    def test_login_wrong_password(self, client):
        """Test login with wrong password."""
        # Register user
        client.post('/register', json={
            'username': 'testuser',
            'password': 'correctpass'
        })
        
        # Login with wrong password
        response = client.post('/login', json={
            'username': 'testuser',
            'password': 'wrongpass'
        })
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid credentials' in data['error']