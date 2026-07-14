"""
=============================================================
Prediction Record Model
Lung Cancer Prediction using Deep Neural Network
=============================================================
Stores each prediction's input features, result, and confidence
score for the user's prediction history.
"""

from datetime import datetime, timezone

from app import db


class Prediction(db.Model):
    """
    Prediction history model.

    Stores the input parameters submitted by the user,
    the model's prediction result, and the confidence score.

    Attributes:
        id              : Primary key
        user_id         : Foreign key linking to the User who made the prediction
        age             : Patient's age
        gender          : Patient's gender (0 = Female, 1 = Male)
        smoking         : Smoking status (0 = No, 1 = Yes)
        yellow_fingers  : Yellow fingers symptom
        anxiety         : Anxiety symptom
        peer_pressure   : Peer pressure factor
        chronic_disease : Chronic disease presence
        fatigue         : Fatigue symptom
        allergy         : Allergy presence
        wheezing        : Wheezing symptom
        alcohol         : Alcohol consumption
        coughing        : Coughing symptom
        shortness_of_breath : Shortness of breath symptom
        swallowing_difficulty: Swallowing difficulty symptom
        chest_pain      : Chest pain symptom
        prediction_result : Model output ('Positive' or 'Negative')
        confidence_score  : Model confidence percentage (0.0 – 100.0)
        created_at      : Timestamp of the prediction
    """

    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    # ----- Patient Information -----
    patient_name = db.Column(db.String(150), nullable=False, default="Unknown")

    # ----- Patient Input Features -----
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)          # 0 = Female, 1 = Male
    smoking = db.Column(db.Integer, nullable=False)          # 0 = No, 1 = Yes
    yellow_fingers = db.Column(db.Integer, nullable=False)
    anxiety = db.Column(db.Integer, nullable=False)
    peer_pressure = db.Column(db.Integer, nullable=False)
    chronic_disease = db.Column(db.Integer, nullable=False)
    fatigue = db.Column(db.Integer, nullable=False)
    allergy = db.Column(db.Integer, nullable=False)
    wheezing = db.Column(db.Integer, nullable=False)
    alcohol_consuming = db.Column(db.Integer, nullable=False)
    coughing = db.Column(db.Integer, nullable=False)
    shortness_of_breath = db.Column(db.Integer, nullable=False)
    swallowing_difficulty = db.Column(db.Integer, nullable=False)
    chest_pain = db.Column(db.Integer, nullable=False)

    # ----- Prediction Output -----
    prediction = db.Column(db.String(20), nullable=True)   # 'Positive' / 'Negative'
    confidence = db.Column(db.Float, nullable=True)          # 0.0 – 100.0

    # ----- Metadata -----
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Prediction #{self.id} by User {self.user_id}: {self.prediction}>"
