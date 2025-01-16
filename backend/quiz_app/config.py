class Config:
    SECRET_KEY = 'your-secret-key-here'  # Change in production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False