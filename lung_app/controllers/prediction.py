"""
=============================================================
Prediction Controller
Lung Cancer Prediction using Deep Neural Network
=============================================================
Handles the prediction form submission, result display, and
prediction history. The actual ML prediction logic will be
implemented in a later phase.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from lung_app import db
from lung_app.models.prediction import Prediction
import os
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# ==================== ML MODEL INITIALIZATION ====================
ml_model = None
ml_scaler = None

# We assume the model is in the 'model' directory at the root of the project.
# lung_app/controllers/prediction.py -> lung_app/controllers -> lung_app -> root -> model
model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'model')
model_path = os.path.join(model_dir, 'lung_model.h5')
scaler_path = os.path.join(model_dir, 'scaler.pkl')

try:
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        ml_model = load_model(model_path)
        ml_scaler = joblib.load(scaler_path)
        print("Successfully loaded ML model and scaler.")
    else:
        print("Warning: ML model or scaler not found at startup.")
except Exception as e:
    print(f"Error loading ML model: {e}")

# Create a blueprint for prediction routes (prefixed with /predict)
prediction_bp = Blueprint("prediction", __name__)


# ==================== PREDICTION FORM ====================

@prediction_bp.route("/", methods=["GET", "POST"])
@login_required
def predict():
    """
    Show the prediction form (GET) or process a prediction (POST).
    The ML model integration will be added in a future phase.
    """

    if request.method == "POST":
        try:
            # ----- Collect patient name and all 15 input features -----
            patient_name = request.form.get("patient_name", "Unknown").strip()
            age = int(request.form.get("age", -1))
            if not (1 <= age <= 120):
                raise ValueError("Age must be between 1 and 120.")
                
            gender = int(request.form.get("gender", -1))
            if gender not in [0, 1]:
                raise ValueError("Invalid gender selection.")
                
            smoking = int(request.form.get("smoking", -1))
            yellow_fingers = int(request.form.get("yellow_fingers", -1))
            anxiety = int(request.form.get("anxiety", -1))
            peer_pressure = int(request.form.get("peer_pressure", -1))
            chronic_disease = int(request.form.get("chronic_disease", -1))
            fatigue = int(request.form.get("fatigue", -1))
            allergy = int(request.form.get("allergy", -1))
            wheezing = int(request.form.get("wheezing", -1))
            alcohol_consuming = int(request.form.get("alcohol_consuming", request.form.get("alcohol", -1)))
            coughing = int(request.form.get("coughing", -1))
            shortness_of_breath = int(request.form.get("shortness_of_breath", -1))
            swallowing_difficulty = int(request.form.get("swallowing_difficulty", -1))
            chest_pain = int(request.form.get("chest_pain", -1))
            
            symptoms = [smoking, yellow_fingers, anxiety, peer_pressure, chronic_disease,
                        fatigue, allergy, wheezing, alcohol_consuming, coughing,
                        shortness_of_breath, swallowing_difficulty, chest_pain]
                        
            if any(s not in [0, 1] for s in symptoms):
                raise ValueError("All clinical symptoms must be either Yes or No.")

        except (ValueError, TypeError) as e:
            flash(f"Invalid input: {str(e)}", "danger")
            return render_template("predict.html", title="Predict")
            
        if ml_model is None or ml_scaler is None:
            flash("Machine learning model is currently unavailable. Please contact support.", "warning")
            return redirect(url_for("auth.dashboard"))

        try:
            # Prepare feature array in the exact order as training
            input_features = [
                gender, age, smoking, yellow_fingers, anxiety, peer_pressure,
                chronic_disease, fatigue, allergy, wheezing, alcohol_consuming,
                coughing, shortness_of_breath, swallowing_difficulty, chest_pain
            ]
            
            features_array = np.array(input_features).reshape(1, -1)
            scaled_features = ml_scaler.transform(features_array)
            
            probability = ml_model.predict(scaled_features)[0][0]
            
            prediction_result = 'Positive' if probability > 0.5 else 'Negative'
            confidence_score = float(probability * 100) if prediction_result == 'Positive' else float((1 - probability) * 100)
            
        except Exception as e:
            flash("An error occurred during prediction computation.", "danger")
            print(f"Prediction error: {str(e)}")
            return redirect(url_for("prediction.predict"))

        # ----- Save the prediction record to the database -----
        record = Prediction(
            user_id=current_user.id,
            patient_name=patient_name,
            age=age,
            gender=gender,
            smoking=smoking,
            yellow_fingers=yellow_fingers,
            anxiety=anxiety,
            peer_pressure=peer_pressure,
            chronic_disease=chronic_disease,
            fatigue=fatigue,
            allergy=allergy,
            wheezing=wheezing,
            alcohol_consuming=alcohol_consuming,
            coughing=coughing,
            shortness_of_breath=shortness_of_breath,
            swallowing_difficulty=swallowing_difficulty,
            chest_pain=chest_pain,
            prediction=prediction_result,
            confidence=confidence_score,
        )

        db.session.add(record)
        db.session.commit()

        flash("Prediction submitted successfully!", "success")
        return redirect(url_for("prediction.result", record_id=record.id))

    # GET request — show prediction form
    return render_template("predict.html", title="Predict")


# ==================== PREDICTION RESULT ====================

@prediction_bp.route("/result/<int:record_id>")
@login_required
def result(record_id):
    """
    Display the result of a specific prediction.
    Only the owner of the prediction can view it.
    """
    record = Prediction.query.get_or_404(record_id)

    # Security check — only allow the owner to view their prediction
    if record.user_id != current_user.id:
        flash("You are not authorized to view this prediction.", "danger")
        return redirect(url_for("auth.dashboard"))

    risk_level = "Low"
    if record.prediction == "Positive":
        if record.confidence and record.confidence >= 75.0:
            risk_level = "High"
        else:
            risk_level = "Medium"

    return render_template("result.html", title="Result", record=record, risk_level=risk_level)


# ==================== PREDICTION HISTORY ====================

@prediction_bp.route("/history")
@login_required
def history():
    """
    Show the full prediction history for the logged-in user.
    Results are ordered by most recent first.
    Supports searching by patient name, sorting, and pagination.
    """
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', 'date_desc')

    query = Prediction.query.filter_by(user_id=current_user.id)

    if search_query:
        query = query.filter(Prediction.patient_name.ilike(f'%{search_query}%'))

    if sort_by == 'name_asc':
        query = query.order_by(Prediction.patient_name.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(Prediction.patient_name.desc())
    elif sort_by == 'conf_asc':
        query = query.order_by(Prediction.confidence.asc())
    elif sort_by == 'conf_desc':
        query = query.order_by(Prediction.confidence.desc())
    elif sort_by == 'date_asc':
        query = query.order_by(Prediction.created_at.asc())
    else:
        query = query.order_by(Prediction.created_at.desc())

    pagination = query.paginate(page=page, per_page=10, error_out=False)
    records = pagination.items

    return render_template("history.html", title="History", records=records, pagination=pagination, search_query=search_query, sort_by=sort_by)


@prediction_bp.route("/delete/<int:record_id>", methods=["POST"])
@login_required
def delete(record_id):
    """
    Delete a prediction record.
    """
    record = Prediction.query.get_or_404(record_id)
    if record.user_id != current_user.id:
        flash("You are not authorized to delete this prediction.", "danger")
        return redirect(url_for("prediction.history"))
        
    db.session.delete(record)
    db.session.commit()
    flash("Prediction deleted successfully.", "success")
    return redirect(url_for("prediction.history"))

@prediction_bp.route("/report/<int:record_id>")
@login_required
def report(record_id):
    """
    Generate a printable prediction report.
    """
    record = Prediction.query.get_or_404(record_id)

    if record.user_id != current_user.id:
        flash("You are not authorized to view this report.", "danger")
        return redirect(url_for("auth.dashboard"))

    risk_level = "Low"
    if record.prediction == "Positive":
        if record.confidence and record.confidence >= 75.0:
            risk_level = "High"
        else:
            risk_level = "Medium"

    return render_template("report.html", title="Print Report", record=record, risk_level=risk_level)
