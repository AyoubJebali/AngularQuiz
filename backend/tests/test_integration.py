import json
import pytest
from quiz_app.models.models import User
from quiz_app import db


class TestIntegration:
    """Integration tests for complete user workflows."""

    def test_complete_user_journey(self, client, app):
        """Test complete user journey: register -> login -> take quiz -> save score -> leaderboard."""

        # 1. Register user
        register_response = client.post(
            "/register", json={"username": "journeyuser", "password": "password123"}
        )
        assert register_response.status_code == 201

        # 2. Login
        login_response = client.post(
            "/login", json={"username": "journeyuser", "password": "password123"}
        )
        assert login_response.status_code == 200

        # 3. Get quiz questions
        quiz_response = client.get("/quizzes?category_ids=1")
        assert quiz_response.status_code == 200
        questions = json.loads(quiz_response.data)
        assert len(questions) == 10

        # 4. Save score
        score_response = client.post(
            "/saveScore", json={"username": "journeyuser", "score": 85}
        )
        assert score_response.status_code == 200

        # 5. Check leaderboard
        leaderboard_response = client.get("/leaderboard")
        assert leaderboard_response.status_code == 200
        leaderboard = json.loads(leaderboard_response.data)

        # User should appear in leaderboard
        user_in_leaderboard = any(
            user["username"] == "journeyuser" and user["score"] == 85
            for user in leaderboard
        )
        assert user_in_leaderboard

    def test_multiple_quiz_attempts(self, client, app):
        """Test user taking multiple quizzes and score accumulation."""

        # Register and login user
        client.post("/register", json={"username": "multiuser", "password": "pass123"})
        client.post("/login", json={"username": "multiuser", "password": "pass123"})

        # Take multiple quizzes
        scores = [75, 90, 65]
        for score in scores:
            response = client.post(
                "/saveScore", json={"username": "multiuser", "score": score}
            )
            assert response.status_code == 200

        # Check final score
        with app.app_context():
            user = User.query.filter_by(username="multiuser").first()
            assert user.total_score == sum(scores)  # 230

    def test_leaderboard_ordering(self, client, app):
        """Test leaderboard correctly orders users by score."""

        users_data = [
            ("user1", 100),
            ("user2", 300),
            ("user3", 150),
            ("user4", 275),
            ("user5", 200),
        ]

        # Create users and scores
        for username, score in users_data:
            client.post("/register", json={"username": username, "password": "pass123"})
            client.post("/saveScore", json={"username": username, "score": score})

        # Check leaderboard
        response = client.get("/leaderboard")
        leaderboard = json.loads(response.data)

        # Should be ordered: user2(300), user4(275), user5(200), user3(150), user1(100)
        expected_order = ["user2", "user4", "user5", "user3", "user1"]
        actual_order = [user["username"] for user in leaderboard]

        assert actual_order == expected_order
