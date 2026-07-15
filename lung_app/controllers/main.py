"""
=============================================================
Main Controller (Public Pages)
Lung Cancer Prediction using Deep Neural Network
=============================================================
Handles the home page, about page, and other public routes.
"""

from flask import Blueprint, render_template

# Create a blueprint for main/public routes
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Render the landing / home page."""
    return render_template("index.html", title="Home")


@main_bp.route("/about")
def about():
    """Render the about page with project information."""
    return render_template("about.html", title="About")
