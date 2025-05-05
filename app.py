from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import os
import mlflow
from waitress import serve

app = Flask(__name__)

# Load model on startup
def load_model():
    model_path = "models/iris_model.pkl"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        print("Warning: Model file not found. Please train the model first.")
        return None

model = load_model()

# Map for class names
iris_species = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.is_json:
            data = request.get_json()
            features = [float(data.get('sepal_length')), 
                         float(data.get('sepal_width')), 
                         float(data.get('petal_length')), 
                         float(data.get('petal_width'))]
        else:
            features = [
                float(request.form.get('sepal_length')),
                float(request.form.get('sepal_width')),
                float(request.form.get('petal_length')),
                float(request.form.get('petal_width'))
            ]
            
        if model is None:
            return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500
            
        prediction = model.predict(np.array([features]))
        species = iris_species[prediction[0]]
        
        if request.is_json:
            return jsonify({
                'prediction': int(prediction[0]),
                'species': species,
                'features': features
            })
        else:
            return render_template('result.html', 
                                   prediction=species, 
                                   features=features)
                                   
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/info', methods=['GET'])
def model_info():
    if model is None:
        return jsonify({'status': 'No model loaded'})
    
    return jsonify({
        'model_type': str(type(model).__name__),
        'features': ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
        'classes': list(iris_species.values())
    })

if __name__ == '__main__':
    print("Starting Iris Classifier Service on port 8080...")
    serve(app, host='0.0.0.0', port=8080) 