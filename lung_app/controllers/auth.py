"""
=============================================================
Auth Controller (Registration, Login, Logout)
Lung Cancer Prediction using Deep Neural Network
=============================================================
Handles user registration, login, logout, and the user dashboard.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from lung_app import db
from lung_app.models.user import User

# Create a blueprint for authentication routes (prefixed with /auth)
auth_bp = Blueprint("auth", __name__)


# ==================== REGISTRATION ====================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Handle user registration.
    GET  → show the registration form.
    POST → validate inputs, create user, redirect to login.
    """

    # Redirect already-authenticated users to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        # Collect form data
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # ----- Validation -----
        errors = []

        if not all([full_name, username, email, password, confirm_password]):
            errors.append("All fields are required.")

        if password != confirm_password:
            errors.append("Passwords do not match.")

        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")

        if User.query.filter_by(username=username).first():
            errors.append("Username is already taken.")

        if User.query.filter_by(email=email).first():
            errors.append("Email is already registered.")

        # If validation fails, flash errors and re-render form
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("register.html", title="Register")

        # ----- Create New User -----
        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    # GET request — show registration form
    return render_template("register.html", title="Register")


# ==================== LOGIN ====================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.
    GET  → show the login form.
    POST → validate credentials, start session, redirect to dashboard.
    """

    # Redirect already-authenticated users to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Look up user by username
        user = User.query.filter_by(username=username).first()

        # Validate credentials
        if user is None or not user.check_password(password):
            flash("Invalid username or password.", "danger")
            return render_template("login.html", title="Login")

        # Log the user in (creates a session)
        login_user(user, remember=True)
        flash(f"Welcome back, {user.full_name}!", "success")

        # Redirect to the page the user originally requested (or dashboard)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("auth.dashboard"))

    # GET request — show login form
    return render_template("login.html", title="Login")


# ==================== LOGOUT ====================

@auth_bp.route("/logout")
@login_required
def logout():
    """Log the user out and redirect to the home page."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


# ==================== DASHBOARD ====================

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    """
    User dashboard — shows a summary of the user's prediction history,
    metrics, and charts.
    """
    from sqlalchemy import func
    from datetime import date
    from lung_app.models.prediction import Prediction

    # Metrics
    total_preds = current_user.predictions.count()
    positive_preds = current_user.predictions.filter_by(prediction="Positive").count()
    negative_preds = current_user.predictions.filter_by(prediction="Negative").count()
    
    # Today's predictions
    # Note: func.date() works in SQLite and MySQL
    today_preds = current_user.predictions.filter(func.date(Prediction.created_at) == date.today()).count()
    
    # Average confidence
    avg_conf = db.session.query(func.avg(Prediction.confidence)).filter(Prediction.user_id == current_user.id).scalar()
    avg_confidence = round(avg_conf, 1) if avg_conf else 0.0

    # Chart Data: Daily Prediction Count
    daily_counts = db.session.query(
        func.date(Prediction.created_at).label('date'),
        func.count(Prediction.id)
    ).filter(Prediction.user_id == current_user.id).group_by(func.date(Prediction.created_at)).order_by(func.date(Prediction.created_at)).all()
    
    chart_dates = [str(r[0]) for r in daily_counts]
    chart_counts = [r[1] for r in daily_counts]
    
    # Chart Data: Average Confidence Trend
    daily_conf = db.session.query(
        func.date(Prediction.created_at).label('date'),
        func.avg(Prediction.confidence)
    ).filter(Prediction.user_id == current_user.id).group_by(func.date(Prediction.created_at)).order_by(func.date(Prediction.created_at)).all()
    
    chart_conf_dates = [str(r[0]) for r in daily_conf]
    chart_conf_values = [round(r[1], 1) for r in daily_conf]

    # Fetch the user's recent prediction history
    recent_predictions = (
        current_user.predictions
        .order_by(None)
        .order_by(Prediction.created_at.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "dashboard.html",
        title="Dashboard",
        predictions=recent_predictions,
        total_preds=total_preds,
        positive_preds=positive_preds,
        negative_preds=negative_preds,
        today_preds=today_preds,
        avg_confidence=avg_confidence,
        chart_dates=chart_dates,
        chart_counts=chart_counts,
        chart_conf_dates=chart_conf_dates,
        chart_conf_values=chart_conf_values
    )
