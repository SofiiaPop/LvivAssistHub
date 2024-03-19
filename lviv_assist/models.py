from datetime import datetime
from lviv_assist import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.surname}', '{self.email}', '{self.image_file})"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_from = db.Column(db.String(20), nullable=False)
    surname_from = db.Column(db.String(20), nullable=False)
    email_from = db.Column(db.String(120), unique=True, nullable=False)
    name_to = db.Column(db.String(20), nullable=False)
    surname_to = db.Column(db.String(20), nullable=False)
    email_to = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.hashtag}', '{self.date_posted}')"
    