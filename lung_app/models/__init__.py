"""
=============================================================
Models Package
Lung Cancer Prediction using Deep Neural Network
=============================================================
Exports all database models for easy access.
"""

from lung_app.models.user import User
from lung_app.models.prediction import Prediction

__all__ = ["User", "Prediction"]
