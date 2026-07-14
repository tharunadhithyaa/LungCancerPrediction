# Lung Cancer Prediction System

A full-stack web application designed to predict the risk of lung cancer using a Deep Neural Network based on clinical symptoms and lifestyle factors. This project features a complete machine learning pipeline integrated into a Flask-based backend with a modern, responsive user interface.

---

## 📌 Project Overview
Lung Cancer is one of the leading causes of cancer-related deaths globally. Early detection is crucial for improving survival rates. This project leverages a Machine Learning model (Deep Neural Network built with TensorFlow/Keras) trained on the **Kaggle Lung Cancer Survey Dataset** to assess a patient's risk based on non-invasive clinical and lifestyle parameters. The system is designed with a user-friendly Dashboard, historical tracking, printable reports, and dynamic risk visualizations.

This project is built as a comprehensive mini-project demonstrating end-to-end Machine Learning deployment in a web application context.

## ✨ Features
- **Deep Neural Network Prediction**: Evaluates 15 clinical and lifestyle features to predict risk.
- **Secure Authentication**: User registration and login utilizing Werkzeug's PBKDF2 password hashing.
- **Interactive Dashboard**: Visualizes historical predictions with Chart.js (Pie, Bar, and Line charts).
- **Prediction History & Management**: Search, sort, paginate, and delete past prediction records.
- **Printable Medical Reports**: Automatically generates clean, printer-friendly risk assessment reports.
- **Responsive Design**: Built with Bootstrap 5, ensuring full compatibility across desktop, tablet, and mobile devices.

---

## 📂 Project Structure
```
LungCancer/
│
├── app/
│   ├── controllers/      # Route handlers (auth, prediction, main)
│   ├── models/           # SQLAlchemy Database Models
│   ├── static/           # CSS, JS, and Images
│   ├── templates/        # HTML Templates (Jinja2)
│   └── __init__.py       # Application Factory
│
├── instance/             # Contains the SQLite Database
├── ml_model/             # Machine Learning Scripts
│   ├── predict.py        # Inference Script
│   └── train_model.py    # Training Script (DNN Pipeline)
│
├── model/                # Saved ML Weights & Scaler
│   ├── lung_model.h5
│   └── scaler.pkl
│
├── app.py                # Main Application Entry Point
├── config.py             # App Configurations
├── requirements.txt      # Python Dependencies
├── survey_lung_cancer.csv# Kaggle Dataset
└── README.md             # Project Documentation
```

---

## 🛠️ Tech Stack
**Frontend:**
- HTML5, CSS3
- Bootstrap 5 (Responsive UI)
- Chart.js (Data Visualization)
- FontAwesome (Icons)

**Backend:**
- Python 3.x
- Flask (Web Framework)
- Flask-SQLAlchemy (ORM)
- Flask-Login (Authentication)

**Machine Learning:**
- TensorFlow / Keras (Deep Neural Network)
- Scikit-Learn (Data Preprocessing, Metrics)
- Pandas, NumPy (Data Handling)

---

## 📊 Dataset Information
The model is trained on the [Kaggle Lung Cancer Survey Dataset](https://www.kaggle.com/datasets).
- **Target Variable:** `LUNG_CANCER` (Positive / Negative)
- **Features (15):** Gender, Age, Smoking, Yellow Fingers, Anxiety, Peer Pressure, Chronic Disease, Fatigue, Allergy, Wheezing, Alcohol Consuming, Coughing, Shortness of Breath, Swallowing Difficulty, Chest Pain.

---

## 🧠 Machine Learning Model
The system uses a Deep Neural Network architecture:
- **Input Layer:** 15 features (Standard Scaled)
- **Hidden Layers:**
  - Dense (64 neurons, ReLU)
  - Dropout (30%)
  - Dense (32 neurons, ReLU)
  - Dense (16 neurons, ReLU)
- **Output Layer:** 1 neuron (Sigmoid Activation for Binary Classification)
- **Optimizer:** Adam
- **Loss Function:** Binary Crossentropy

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/LungCancerPrediction.git
cd LungCancerPrediction
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Python Requirements
```bash
pip install -r requirements.txt
```

### 4. Database Setup
The SQLite database is configured to build itself automatically. Upon running the Flask application for the first time, it will generate the `instance/lungcancer.db` file.

---

## 🏋️ How to Train the Model
If you wish to retrain the neural network, execute the training script:
```bash
python ml_model/train_model.py
```
This script will parse the `survey_lung_cancer.csv`, retrain the DNN, and output the updated `lung_model.h5` and `scaler.pkl` to the `/model` directory.

---

## 🚀 How to Run the Flask Application
Start the Flask server using:
```bash
python app.py
```
Open your web browser and navigate to: `http://127.0.0.1:5000`

---

## 📸 Screenshots

| Dashboard View | Prediction Form |
| :---: | :---: |
| *(Placeholder for Dashboard Screenshot)* | *(Placeholder for Prediction Form Screenshot)* |

| Result Report | Printable Document |
| :---: | :---: |
| *(Placeholder for Result Report Screenshot)* | *(Placeholder for Print View Screenshot)* |

---

## 🔮 Future Enhancements
- Integration of a larger clinical dataset (e.g., CT Scan Image Processing via CNNs).
- Multi-role access (Admin vs Doctor vs Patient).
- Exportable analytics (PDF/CSV Generation) directly from the Dashboard.

---

## ✍️ Author
Designed and Developed as a College Mini-Project.
*Your Name Here*
# LungCancerPrediction
