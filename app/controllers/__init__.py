"""
=============================================================
Controllers Package
Lung Cancer Prediction using Deep Neural Network
=============================================================
Exports all Flask blueprints (controllers).
"""

from app.controllers.main import main_bp
from app.controllers.auth import auth_bp
from app.controllers.prediction import prediction_bp

__all__ = ["main_bp", "auth_bp", "prediction_bp"]
