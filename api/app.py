from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Load the model and encoders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
MODEL_PATH = os.path.join(PROJECT_ROOT, 'picklefiles', 'flight_price_model.pkl')
ENCODERS_PATH = os.path.join(PROJECT_ROOT, 'picklefiles', 'label_encoders.pkl')
# Load model
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# Load encoders
with open(ENCODERS_PATH, 'rb') as f:
    label_encoders = pickle.load(f)

print("✅ Model and encoders loaded successfully!")

@app.route('/')
def home():
    return jsonify({
        "message": "Voyage Analytics - Flight Price Prediction API",
        "status": "running",
        "endpoints": {
            "/predict": "POST - Predict flight price"
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.get_json()
        
        # Required features
        required_fields = ['flightType', 'time', 'distance', 'agency', 'from', 'to', 'month', 'dayofweek', 'quarter']
        
        # Validate input
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        # Create DataFrame
        input_df = pd.DataFrame([{
            'flightType': data['flightType'],
            'time': float(data['time']),
            'distance': float(data['distance']),
            'agency': data['agency'],
            'from': data['from'],
            'to': data['to'],
            'month': int(data['month']),
            'dayofweek': int(data['dayofweek']),
            'quarter': int(data['quarter'])
        }])
        
        # Encode categorical variables
        categorical_columns = ['flightType', 'agency', 'from', 'to']
        for col in categorical_columns:
            input_df[col] = label_encoders[col].transform(input_df[col])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        return jsonify({
            "success": True,
            "predicted_price": round(float(prediction), 2),
            "input": data
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)