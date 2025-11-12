from quiz_app import create_app, db
from flask_cors import CORS 

app = create_app()
# Configure CORS
cors = CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:4200"],  # Angular dev server
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)