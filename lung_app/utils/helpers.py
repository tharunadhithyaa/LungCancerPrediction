"""
=============================================================
Utility Helpers
Lung Cancer Prediction using Deep Neural Network
=============================================================
Common helper functions used across the application.
"""


def format_confidence(score):
    """
    Format a confidence score as a percentage string.

    Args:
        score (float): Confidence score between 0.0 and 100.0.

    Returns:
        str: Formatted string like '87.5%'.
    """
    if score is None:
        return "N/A"
    return f"{score:.1f}%"


def get_risk_level(confidence):
    """
    Categorize the confidence score into a human-readable risk level.

    Args:
        confidence (float): Confidence score between 0.0 and 100.0.

    Returns:
        tuple: (risk_label, bootstrap_color_class)
    """
    if confidence is None:
        return ("Unknown", "secondary")
    elif confidence >= 75.0:
        return ("High Risk", "danger")
    elif confidence >= 50.0:
        return ("Moderate Risk", "warning")
    elif confidence >= 25.0:
        return ("Low Risk", "info")
    else:
        return ("Minimal Risk", "success")


# Feature labels for display in templates
FEATURE_LABELS = {
    "age": "Age",
    "gender": "Gender",
    "smoking": "Smoking",
    "yellow_fingers": "Yellow Fingers",
    "anxiety": "Anxiety",
    "peer_pressure": "Peer Pressure",
    "chronic_disease": "Chronic Disease",
    "fatigue": "Fatigue",
    "allergy": "Allergy",
    "wheezing": "Wheezing",
    "alcohol": "Alcohol Consumption",
    "coughing": "Coughing",
    "shortness_of_breath": "Shortness of Breath",
    "swallowing_difficulty": "Swallowing Difficulty",
    "chest_pain": "Chest Pain",
}
