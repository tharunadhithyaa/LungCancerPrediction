"""
=============================================================
Models Package
Lung Cancer Prediction using Deep Neural Network
=============================================================
Exports all database models for easy access.
"""

from app.models.user import User
from app.models.prediction import Prediction

__all__ = ["User", "Prediction"]
