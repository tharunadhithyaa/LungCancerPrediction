import os
import numpy as np
import joblib
from tensorflow.keras.models import load_model

class LungCancerPredictor:
    def __init__(self):
        """
        Initialize the predictor by loading the saved model and scaler.
        """
        model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model')
        model_path = os.path.join(model_dir, 'lung_model.h5')
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            raise FileNotFoundError("Model or scaler not found. Please run train_model.py first.")
            
        self.model = load_model(model_path)
        self.scaler = joblib.load(scaler_path)
        
    def predict(self, input_data):
        """
        Make a prediction based on input features.
        
        Args:
            input_data (list or numpy array): A 1D array of 15 features matching the 
            training data order:
            [GENDER, AGE, SMOKING, YELLOW_FINGERS, ANXIETY, PEER_PRESSURE, 
             CHRONIC DISEASE, FATIGUE, ALLERGY, WHEEZING, ALCOHOL CONSUMING, 
             COUGHING, SHORTNESS OF BREATH, SWALLOWING DIFFICULTY, CHEST PAIN]
             
             Note: GENDER (0=F, 1=M), all other symptoms (0=No, 1=Yes)
             
        Returns:
            dict: Containing 'prediction' ('Positive' or 'Negative') and 'confidence' (percentage)
        """
        # Convert to numpy array and reshape to (1, 15)
        features = np.array(input_data).reshape(1, -1)
        
        # Scale features using the saved scaler
        scaled_features = self.scaler.transform(features)
        
        # Make prediction
        probability = self.model.predict(scaled_features)[0][0]
        
        # Interpret result
        result = 'Positive' if probability > 0.5 else 'Negative'
        confidence = float(probability * 100) if result == 'Positive' else float((1 - probability) * 100)
        
        return {
            'prediction': result,
            'confidence': confidence
        }

if __name__ == "__main__":
    # Example usage
    try:
        predictor = LungCancerPredictor()
        # Example input (Male, 69 years, Smoking, etc.)
        # GENDER(M=1), AGE(69), SMOKING(1), YELLOW_FINGERS(1), ANXIETY(1), 
        # PEER_PRESSURE(0), CHRONIC DISEASE(0), FATIGUE(1), ALLERGY(0), 
        # WHEEZING(1), ALCOHOL CONSUMING(1), COUGHING(1), SHORTNESS OF BREATH(1), 
        # SWALLOWING DIFFICULTY(1), CHEST PAIN(1)
        sample_input = [1, 69, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1]
        
        print("Making test prediction...")
        result = predictor.predict(sample_input)
        print(f"Result: {result['prediction']}")
        print(f"Confidence: {result['confidence']:.2f}%")
        
    except Exception as e:
        print(f"Error during prediction: {e}")
