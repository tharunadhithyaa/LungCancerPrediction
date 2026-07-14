"""
=============================================================
Configuration Module
Lung Cancer Prediction using Deep Neural Network
=============================================================
Contains application configuration classes for different
environments (Development, Testing, Production).
"""

import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class.
    Contains default settings shared across all environments.
    """

    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get("SECRET_KEY", "lung-cancer-prediction-secret-key-2026")

    # SQLite database URI — stored in the 'instance' folder
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'lung_cancer.db')}"
    )

    # Disable SQLAlchemy event tracking for better performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload folder for any future file uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    # Maximum upload size: 16 MB
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'test.db')}"


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False


# Dictionary to map environment names to config classes
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
