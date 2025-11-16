"""Test data fixtures for the quiz application."""

SAMPLE_QUIZ_DATA = [
    {
        "id": 1,
        "name": "General Knowledge",
        "questions": [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correctIndex": 2,
            },
            {
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "correctIndex": 1,
            },
            # Add more questions to reach 10+
        ],
    },
    {
        "id": 2,
        "name": "Science",
        "questions": [
            {
                "question": "What is the chemical symbol for water?",
                "options": ["H2O", "CO2", "NaCl", "O2"],
                "correctIndex": 0,
            },
            # Add more questions
        ],
    },
]

SAMPLE_USERS = [
    {"username": "alice", "password": "alice123", "score": 250},
    {"username": "bob", "password": "bob123", "score": 180},
    {"username": "charlie", "password": "charlie123", "score": 320},
]
