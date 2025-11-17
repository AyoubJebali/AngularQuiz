"""Quiz routes module.

This module contains all quiz-related API endpoints including quiz data retrieval,
leaderboard, and score saving functionality.
"""

import json
import os
import random
from typing import Dict, List, Any, Optional

from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user

from ..models.models import User, db

bp = Blueprint("quiz_blueprint", __name__)

# Get the absolute path to the directory where your script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the absolute path to quizzes.json one level up
JSON_PATH = os.path.join(BASE_DIR, "..", "quizzes.json")

# Normalize the path (resolves ../ properly)
QUIZ_DATA_PATH = os.path.normpath(JSON_PATH)

# Constants
MIN_QUESTIONS_REQUIRED = 10
MAX_LEADERBOARD_USERS = 10


def load_quiz_data(file_path: str) -> List[Dict[str, Any]]:
    """Load quiz categories and questions from the JSON file.

    Args:
        file_path: Path to the quiz data JSON file

    Returns:
        List of quiz categories with questions, empty list if error occurs
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        current_app.logger.error("Quiz data file not found: %s", file_path)
        return []
    except json.JSONDecodeError:
        current_app.logger.error("Error decoding JSON from file: %s", file_path)
        return []
    except IOError as error:
        current_app.logger.error("IO error reading file %s: %s", file_path, error)
        return []


def _parse_category_ids(category_ids_str: str) -> Optional[List[int]]:
    """Parse category IDs from query string.

    Args:
        category_ids_str: Comma-separated category IDs string

    Returns:
        List of category IDs or None if parsing fails
    """
    try:
        return list(map(int, category_ids_str.split(",")))
    except (ValueError, AttributeError):
        return None


def _filter_categories_by_ids(data: List[Dict], category_ids: List[int]) -> List[Dict]:
    """Filter categories based on provided category IDs.

    Args:
        data: List of all categories
        category_ids: List of category IDs to filter by

    Returns:
        List of filtered categories
    """
    return [category for category in data if category["id"] in category_ids]


def _collect_questions_from_categories(categories: List[Dict]) -> List[Dict]:
    """Collect all questions from selected categories.

    Args:
        categories: List of category dictionaries

    Returns:
        List of all questions from the categories
    """
    questions = []
    for category in categories:
        if "questions" in category:
            questions.extend(category["questions"])
    return questions


def _format_quiz_response(questions: List[Dict]) -> List[Dict]:
    """Format questions for API response.

    Args:
        questions: List of question dictionaries

    Returns:
        List of formatted question dictionaries
    """
    return [
        {
            "question": question["question"],
            "options": question["options"],
            "correctIndex": question["correctIndex"],
        }
        for question in questions
    ]


@bp.route("/quizzes", methods=["GET"])
def get_quizzes():
    """Get quiz questions based on category IDs.

    Returns:
        JSON response with selected quiz questions or error message
    """
    # Get category IDs from the query parameter
    category_ids_str = request.args.get("category_ids")
    if not category_ids_str:
        return jsonify({"error": "Category IDs are required"}), 400

    # Parse category IDs
    category_ids = _parse_category_ids(category_ids_str)
    if category_ids is None:
        return jsonify({"error": "Invalid category IDs format"}), 400

    current_app.logger.info("Requested category IDs: %s", category_ids)

    # Load quiz data from the JSON file
    data = load_quiz_data(QUIZ_DATA_PATH)
    if not data:
        return jsonify({"error": "Failed to load quiz data"}), 500

    # Filter categories based on provided IDs
    selected_categories = _filter_categories_by_ids(data, category_ids)
    if not selected_categories:
        return jsonify({"error": "No categories found with the given IDs"}), 404

    # Collect all questions from selected categories
    questions = _collect_questions_from_categories(selected_categories)

    # Check if there are enough questions
    if len(questions) < MIN_QUESTIONS_REQUIRED:
        return jsonify(
            {
                "error": f"Not enough questions in the selected categories. "
                f"Need at least {MIN_QUESTIONS_REQUIRED}, found {len(questions)}"
            }
        ), 400

    # Randomly select questions from the combined list
    selected_questions = random.sample(questions, MIN_QUESTIONS_REQUIRED)

    # Format and return response
    formatted_questions = _format_quiz_response(selected_questions)
    return jsonify(formatted_questions)


@bp.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    """Get top users by total score.

    Returns:
        JSON response with leaderboard data
    """
    try:
        users = (
            User.query.order_by(User.total_score.desc())
            .limit(MAX_LEADERBOARD_USERS)
            .all()
        )

        current_app.logger.info("Leaderboard data requested.")

        leaderboard_data = [
            {
                "username": user.username,
                "score": user.total_score,
            }
            for user in users
        ]

        return jsonify(leaderboard_data)

    except Exception as error:
        current_app.logger.error("Error fetching leaderboard: %s", error)
        return jsonify({"error": "Failed to fetch leaderboard"}), 500


@bp.route("/saveScore", methods=["POST"])
def save_score():
    """Save user's quiz score.

    Returns:
        JSON response with success or error message
    """
    try:
        data = request.get_json()

        # Validate request data
        if not data or "username" not in data or "score" not in data:
            return jsonify({"error": "Username and score are required"}), 400

        username = data["username"]
        score = data["score"]

        # Validate score is a number
        if not isinstance(score, (int, float)) or score < 0:
            return jsonify({"error": "Score must be a non-negative number"}), 400

        # Find user
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update user's total score
        user.total_score += score
        db.session.commit()

        current_app.logger.info("Score %s saved for user %s.", score, username)
        return jsonify({"message": "Score saved successfully"}), 200

    except Exception as error:
        current_app.logger.error("Error saving score: %s", error)
        db.session.rollback()
        return jsonify({"error": "Failed to save score"}), 500
