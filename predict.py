import mlflow
import pandas as pd
import numpy as np
import joblib
import sys

def load_model_from_mlflow(run_id, model_path="model"):
    """Load model from MLflow run"""
    model = mlflow.sklearn.load_model(f"runs:/{run_id}/{model_path}")
    return model

def load_model_local(model_path="models/iris_model.pkl"):
    """Load model from local file"""
    return joblib.load(model_path)

def predict(model, data):
    """Make predictions with the model"""
    return model.predict(data)

def main():
    # Sample data (4 features matching Iris dataset)
    if len(sys.argv) > 4:
        # Use command line arguments as features
        sample_data = np.array([[float(sys.argv[1]), float(sys.argv[2]), 
                                 float(sys.argv[3]), float(sys.argv[4])]])
    else:
        # Default sample
        sample_data = np.array([[5.1, 3.5, 1.4, 0.2]])  # Example of Iris setosa
    
    print(f"Input features: {sample_data[0]}")
    
    try:
        # Try to load from local file first
        model = load_model_local()
        print("Model loaded from local file")
    except:
        print("Could not load model from local file")
        run_id = input("Enter MLflow run_id to load model (or press Enter to exit): ")
        if run_id:
            model = load_model_from_mlflow(run_id)
            print(f"Model loaded from MLflow run {run_id}")
        else:
            print("No model available. Please train the model first.")
            return
    
    # Make prediction
    prediction = predict(model, sample_data)
    
    # Map prediction to Iris species
    iris_species = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
    result = iris_species[prediction[0]]
    
    print(f"Predicted class: {prediction[0]} ({result})")

if __name__ == "__main__":
    main() 