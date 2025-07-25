from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)  # Store hashed passwords
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    country = db.Column(db.String(64), nullable=True)
    contact_email = db.Column(db.String(120), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)
    ratings = db.relationship('Rating', back_populates='author', lazy=True, overlaps="user_ratings,author")  # Refined overlaps
    housekeepers = db.relationship('Housekeeper', back_populates='user', lazy=True)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Checks the hashed password."""
        return check_password_hash(self.password, password)


class Housekeeper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    passport_number = db.Column(db.String(50), unique=True)
    nationality = db.Column(db.String(100))
    working_countries = db.Column(db.String(500), nullable=False)  # Store as a comma-separated string
    note = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='housekeepers', lazy=True)
    ratings = db.relationship('Rating', back_populates='evaluated_housekeeper', lazy=True)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cleaning = db.Column(db.Integer, nullable=False)  # Use Integer for ratings
    timing = db.Column(db.Integer, nullable=False)
    cooking = db.Column(db.Integer, nullable=False)
    childcare = db.Column(db.Integer, nullable=False)
    respect = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    housekeeper_id = db.Column(db.Integer, db.ForeignKey('housekeeper.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    author = db.relationship('User', back_populates='ratings', overlaps="user_ratings,author")  # Refined overlaps
    evaluated_housekeeper = db.relationship('Housekeeper', back_populates='ratings', lazy=True)