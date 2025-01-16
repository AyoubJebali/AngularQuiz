from flask import Blueprint, jsonify,request
from flask_login import login_required, current_user
from ..models.models import User, db
import json
import random 

bp = Blueprint('quiz_blueprint', __name__)
path = 'C:\\Users\\ayoub\Desktop\\angularProj\\PyhtonBackend\\quiz_app\\quizzes.json'
# Load quiz categories and questions from the JSON file
def load_quiz_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON. Please check the file format.")
        return []




@bp.route('/quizzes', methods=['GET'])
def get_quizzes():
    # Get category IDs from the query parameter (e.g., /quizzes?category_ids=1,2,3)
    category_ids = request.args.get('category_ids')
    if not category_ids:
        return jsonify({"error": "Category IDs are required"}), 400
    # Convert the category_ids string into a list of integers
    category_ids = list(map(int, category_ids.split(',')))
    print(category_ids)
    
    # Load quiz data from the JSON file
    data = load_quiz_data(path)

    print(type(data))
     # Filter the categories based on the provided category_ids
    selected_categories = [category for category in data if category['id'] in category_ids]


    # Check if any categories were found
    if not selected_categories:
        return jsonify({"error": "No categories found with the given IDs"}), 404

    # Collect all questions from the selected categories
    questions = []
    for category in selected_categories:
        questions.extend(category['questions'])  # Assuming 'questions' is a list within each category

    # Check if there are enough questions
    if len(questions) < 10:
        return jsonify({"error": "Not enough questions in the selected categories"}), 400

    # Randomly select 10 questions from the combined list
    selected_questions = random.sample(questions, 10)

    # Prepare the response
    response = {
        'selected_questions': [{
            'question': question['question'],  # Access question text
            'options': question['options'],  # Access options list
            'correctIndex': question['correctIndex']  # Access correct answer index
        } for question in selected_questions]
    }

    return jsonify(response["selected_questions"])



@bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    users = User.query.order_by(User.total_score.desc()).limit(10).all()
    return jsonify([{
        'username': user.username,
        'score': user.total_score,
    } for user in users])

@bp.route('/saveScore', methods=['POST'])
def save_score():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    user.total_score += data['score']
    db.session.commit()
    return jsonify({'message': 'Score saved successfully'}), 200
