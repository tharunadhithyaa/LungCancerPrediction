"""
=============================================================
Controllers Package
Lung Cancer Prediction using Deep Neural Network
=============================================================
Exports all Flask blueprints (controllers).
"""

from lung_app.controllers.main import main_bp
from lung_app.controllers.auth import auth_bp
from lung_app.controllers.prediction import prediction_bp

__all__ = ["main_bp", "auth_bp", "prediction_bp"]
