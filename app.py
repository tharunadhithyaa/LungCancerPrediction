"""
=============================================================
Entry Point — app.py
Lung Cancer Prediction using Deep Neural Network
=============================================================
Creates and runs the Flask application.
Run this file to start the development server:
    python app.py
"""

from app import create_app

# Create application instance using the development config
app = create_app("development")

if __name__ == "__main__":
    # Run the Flask development server
    # Host 0.0.0.0 allows access from external devices on the network
    app.run(host="0.0.0.0", port=5000, debug=True)
