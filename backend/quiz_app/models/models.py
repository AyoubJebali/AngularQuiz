from datetime import datetime
from flask_login import UserMixin
from .. import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    total_score = db.Column(db.Integer, default=0)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
