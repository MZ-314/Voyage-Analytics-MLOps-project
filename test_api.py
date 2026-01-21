import requests
import json

# Test data (same as first row from our training data)
test_data = {
    "flightType": "firstClass",
    "time": 1.76,
    "distance": 676.53,
    "agency": "FlyingDrops",
    "from": "Recife (PE)",
    "to": "Florianopolis (SC)",
    "month": 9,
    "dayofweek": 3,
    "quarter": 3
}

print("Testing Flight Price Prediction API...")
print("\nInput Data:")
print(json.dumps(test_data, indent=2))

# Make prediction request
response = requests.post('http://127.0.0.1:5000/predict', json=test_data)

print("\n" + "="*50)
print("Status Code:", response.status_code)
print("\nAPI Response:")
print(json.dumps(response.json(), indent=2))