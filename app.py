from flask import Flask, request, render_template
import pickle
import numpy as np

# Load and verify the model
with open('model.pickle', 'rb') as f:
    model = pickle.load(f)['model']
    print("Model loaded successfully!")

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
        
        # Reshape for LSTM model input
        features_reshaped = features.reshape(1, 1, 15)  # (batch_size=1, timesteps=1, features=15)
        
        # Make prediction using the loaded model
        prediction = model.predict(features_reshaped)
        print(f"Model prediction: {prediction}")

        # Format the prediction for display
        prediction_text = f"Predicted Close Price: {prediction[0][0]}"
    except Exception as e:
        prediction_text = f"Error: {str(e)}"

    # Return the prediction to the HTML template
    return render_template('index.html', prediction_text=prediction_text)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
