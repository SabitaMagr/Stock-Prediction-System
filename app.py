from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd

# Load and verify the model
with open('model.pickle', 'rb') as f:
    model = pickle.load(f)['model']
    print("Model loaded successfully!")
    print(f"Model type: {type(model)}")
    print(model)
    print(f"Model input shape: {model.input_shape}")

# Initialize Flask app
app = Flask(__name__)

# Define the home route
@app.route('/')
def home():
    return render_template('index.html')

# Define the predict route
@app.route('/predict', methods=['POST'])
def predict():
    print("Successfully received a request!")
    # Get data from the form
    data = request.form
    print(f"Data: {data}")

    try:
        # Extract features from the form data
        features = np.array([
            float(data['open']),
            float(data['high']),
            float(data['low']),
            float(data['volume']),
            float(data['macd']),
            float(data['rsi']),
            float(data['atr']),
            float(data['mfi']),
            float(data['cpi']),
            float(data['usdx']),
            float(data['ir']),
            float(data['tb']),
            float(data['effr']),
            float(data['rmt']),
            float(data['score'])
        ])

        # Check if the features array size matches the model's expected feature size
        if features.size != 17:
            raise ValueError(f"Expected 17 features but got {features.size}")

        # Reshape features to match the model input
        # Here we assume that each sequence is a 1D array of length 17 and there are 5 timesteps
        features_reshaped = np.repeat(features.reshape(1, 17), 5, axis=0).reshape(1, 5, 17)

        # Make prediction using the loaded model
        prediction = model.predict(features_reshaped)
        print(f"Model prediction: {prediction}")

        # Format the prediction for display
        prediction_text = f"Predicted Value: {prediction[0][0]}"
    except Exception as e:
        prediction_text = f"Error: {str(e)}"

    # Return the prediction to the HTML template
    return render_template('index.html', prediction_text=prediction_text)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
