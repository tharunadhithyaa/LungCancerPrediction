"""
=============================================================
Application Factory
Lung Cancer Prediction using Deep Neural Network
=============================================================
Initializes the Flask application using the Application Factory
pattern. Registers extensions, blueprints, and creates database
tables on first run.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

from config import config_by_name

# ----- Initialize Extensions (without binding to app yet) -----
db = SQLAlchemy()
login_manager = LoginManager()

# Configure Flask-Login defaults
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"


def create_app(config_name="default"):
    """
    Application factory function.

    Args:
        config_name (str): Configuration environment name
                           ('development', 'testing', 'production', 'default').

    Returns:
        Flask: Configured Flask application instance.
    """

    # Create Flask instance with template and static folders
    app = Flask(
        __name__,
        template_folder="../app/templates",
        static_folder="../app/static",
    )

    # Load configuration from config.py
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    # Ensure the instance folder exists (for SQLite database)
    instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance")
    os.makedirs(instance_path, exist_ok=True)

    # Ensure the uploads folder exists
    os.makedirs(app.config.get("UPLOAD_FOLDER", "uploads"), exist_ok=True)

    # ----- Initialize Extensions with App -----
    db.init_app(app)
    login_manager.init_app(app)

    # ----- Register Blueprints (Controllers) -----
    from app.controllers.main import main_bp
    from app.controllers.auth import auth_bp
    from app.controllers.prediction import prediction_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(prediction_bp, url_prefix="/predict")

    # ----- Create Database Tables -----
    with app.app_context():
        from app.models import user, prediction  # noqa: F401 — import to register models
        db.create_all()

    return app
