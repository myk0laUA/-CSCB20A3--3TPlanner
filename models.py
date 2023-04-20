from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
import os
from werkzeug.utils import secure_filename
from flask import url_for

# represents the User table in the database with columns for id, username, email,
#  password hash, number of tokens, dark mode boolean, and profile picture path.
#  It has a one-to-many relationship with Task table. The class provides methods to
#  set and check password, save a profile picture, and get the path to the profile picture.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    tokens = db.Column(db.Integer, default=0)
    dark_mode = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(120), nullable=False, default='static/profile_pics/default.png')

    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save_profile_picture(self, picture):
        filename = secure_filename(picture.filename)
        picture_path = os.path.join('static/profile_pics', filename)
        picture.save(picture_path)
        self.profile_picture = filename
    
    def get_profile_picture(self):
        return url_for('static', filename=f'profile_pics/{self.profile_picture}')

#  Represents the Task table in the database with columns for id, title, duration, start_time, completed boolean,
#  timestamp, and user_id. It has a many-to-one relationship with the User table.
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, index=True, default=None, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Task('{self.title}', '{self.duration}', '{self.completed}')"
    
#  Represents the Tip table in the database with columns for id, content, timestamp, user_id, and comments.
#  It has a many-to-one relationship with User table and a one-to-many relationship with the Comment table.
#  It provides a method to represent itself as a string.    
class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tips', lazy=True))
    comments = db.relationship('Comment', back_populates='parent_tip', lazy=True)

    def __repr__(self):
        return f"Tip('{self.content}', '{self.timestamp}')"

#  Represents the Comment table in the database with columns for id, content, timestamp, user_id, and tip_id.
#  It has a many-to-one relationship with the User and Tip tables. It provides a method to represent itself as a string.
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tip_id = db.Column(db.Integer, db.ForeignKey('tip.id'), nullable=False)
    parent_tip = db.relationship('Tip', back_populates='comments')
    user = db.relationship('User', backref=db.backref('comments', lazy=True))  # Add this line

    def __repr__(self):
        return f"Comment('{self.content}', '{self.timestamp}')"


# Represents the Like table in the database with columns for id, user_id, and tip_id.
# It has a many-to-one relationship with the User and Tip tables. It provides a method to represent itself as a string.
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tip_id = db.Column(db.Integer, db.ForeignKey('tip.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    tip = db.relationship('Tip', backref=db.backref('likes', lazy=True))

    def __repr__(self):
        return f"Like(user_id='{self.user_id}', tip_id='{self.tip_id}')"

# The function is used by Flask-Login to get a user from the database based 
# on their ID. It returns a User object with the given ID.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
