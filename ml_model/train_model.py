import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input

import matplotlib.pyplot as plt

# 1. Load the dataset
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'survey_lung_cancer.csv')
df = pd.read_csv(data_path)

# 2. Inspect and clean the data
df.drop_duplicates(inplace=True)

# 3. Handle missing values
df.dropna(inplace=True)

# 4. Encode categorical features
# GENDER: M -> 1, F -> 0
df['GENDER'] = df['GENDER'].map({'M': 1, 'F': 0})

# LUNG_CANCER: YES -> 1, NO -> 0
df['LUNG_CANCER'] = df['LUNG_CANCER'].map({'YES': 1, 'NO': 0})

# Symptoms are 1 (No), 2 (Yes). We convert them to 0 (No), 1 (Yes)
symptom_cols = [col for col in df.columns if col not in ['GENDER', 'AGE', 'LUNG_CANCER']]
for col in symptom_cols:
    df[col] = df[col] - 1

# 5. Separate features and target label
X = df.drop('LUNG_CANCER', axis=1)
y = df['LUNG_CANCER']

# 6. Split the data into training and testing sets (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 7. Normalize the features using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 8. Build a Deep Neural Network using TensorFlow/Keras
model = Sequential([
    Input(shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

# 9. Compile using Adam Optimizer, Binary Crossentropy, Accuracy
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 10. Train the model
print("Training model...")
history = model.fit(X_train_scaled, y_train, epochs=50, batch_size=16, validation_split=0.2, verbose=1)

# 11. Evaluate using Accuracy, Precision, Recall, F1 Score, ROC AUC
y_pred_prob = model.predict(X_test_scaled)
y_pred = (y_pred_prob > 0.5).astype(int).flatten()

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_prob)

print(f"\nModel Evaluation Metrics:")
print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC AUC:   {roc_auc:.4f}")

# 11b. Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:")
print(cm)

# 11c. Classification Report
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Negative', 'Positive']))

# 11d. Training Accuracy vs Validation Accuracy Graph
plt.figure(figsize=(10, 5))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training Accuracy vs Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# 11e. Training Loss vs Validation Loss Graph
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training Loss vs Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.show()

# 12. Save the trained model
model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model')
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, 'lung_model.h5')
model.save(model_path)
print(f"\nModel saved to {model_path}")

# 13. Save preprocessing objects
scaler_path = os.path.join(model_dir, 'scaler.pkl')
joblib.dump(scaler, scaler_path)
print(f"Scaler saved to {scaler_path}")
print("Training complete.")

