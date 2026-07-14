"""
=============================================================
User Model
Lung Cancer Prediction using Deep Neural Network
=============================================================
Defines the User table for authentication and profile data.
Uses Flask-Login's UserMixin for session management.
"""

from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """
    User model for authentication and authorization.

    Attributes:
        id          : Primary key
        username    : Unique username
        email       : Unique email address
        password_hash: Hashed password (never store plain text)
        full_name   : User's display name
        created_at  : Account creation timestamp
        is_active   : Whether the account is active
        predictions : Relationship to PredictionRecord
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)

    # One-to-many relationship: one user can have many predictions
    predictions = db.relationship(
        "Prediction", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    # ---- Password Handling ----

    def set_password(self, password):
        """Hash and store the password. Never stores plain text."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify a plain-text password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


# ----- Flask-Login User Loader Callback -----
@login_manager.user_loader
def load_user(user_id):
    """Load a user by their ID for Flask-Login session management."""
    return db.session.get(User, int(user_id))
