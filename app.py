"""
=============================================================
Entry Point — app.py
Lung Cancer Prediction using Deep Neural Network
=============================================================
Creates and runs the Flask application.
Run this file to start the development server:
    python app.py
"""

import os
from lung_app import create_app

# Create application instance (reads FLASK_CONFIG env var, defaults to development)
app = create_app(os.environ.get("FLASK_CONFIG", "development"))

if __name__ == "__main__":
    # Run the Flask development server
    # Host 0.0.0.0 allows access from external devices on the network
    app.run(host="0.0.0.0", port=5000, debug=True)
