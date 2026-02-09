import mlflow
import mlflow.sklearn
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import os

# Set MLFlow tracking URI
mlflow.set_tracking_uri("file:./mlflow_tracking")
mlflow.set_experiment("flight-price-prediction")

print("="*60)
print("MLFLOW MODEL TRACKING - FLIGHT PRICE PREDICTION")
print("="*60)

# Load the existing model
MODEL_PATH = os.path.join('picklefiles', 'flight_price_model.pkl')
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

print("\n✅ Model loaded successfully!")

# Start MLFlow run
with mlflow.start_run(run_name="RandomForest_Flight_Price"):
    
    # Log parameters
    mlflow.log_param("model_type", "RandomForestRegressor")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 20)
    mlflow.log_param("min_samples_split", 5)
    mlflow.log_param("min_samples_leaf", 2)
    
    # Log metrics (from our previous training results)
    mlflow.log_metric("test_mae", 0.00)
    mlflow.log_metric("test_rmse", 0.03)
    mlflow.log_metric("test_r2_score", 1.0000)
    mlflow.log_metric("train_mae", 0.00)
    mlflow.log_metric("train_rmse", 0.02)
    mlflow.log_metric("train_r2_score", 1.0000)
    
    # Log the model
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="flight_price_predictor"
    )
    
    # Log additional info
    mlflow.set_tag("dataset", "flights.csv")
    mlflow.set_tag("project", "Voyage Analytics")
    mlflow.set_tag("model_version", "v1.0")
    
    print("\n✅ Model logged to MLFlow!")
    print(f"Run ID: {mlflow.active_run().info.run_id}")

print("\n" + "="*60)
print("MLFlow tracking complete!")
print("="*60)
print("\nTo view the MLFlow UI, run:")
print("  mlflow ui")
print("\nThen open: http://127.0.0.1:5000")
print("="*60)