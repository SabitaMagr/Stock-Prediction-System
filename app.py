import flask
import pickle
import pandas as pd
import numpy as np
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sklearn.preprocessing import StandardScaler
from flask import session

app = Flask(__name__)

# Loads the trained model
with open('model.pickle', 'rb') as f:
    clf_lr = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Extracts features from form
        features = [float(x) for x in request.form.values()]
        features = np.array([features])

        # Make prediction
        prediction = clf_lr.predict(features)

        return render_template('index.html', prediction_text=f'Predicted Stock Price: {prediction[0]}')

if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask, request, render_template

# app = Flask(__name__)

# # Mock function to replace model prediction
# def mock_predict(features):
#     # Example: return a fixed value or some computed value
#     return [123.45]  # Replace with desired mock value or computation

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     if request.method == 'POST':
#         # Extracts features from form
#         features = [float(x) for x in request.form.values()]
#         features = np.array([features])

#         # Make prediction using mock function
#         prediction = mock_predict(features)

#         return render_template('index.html', prediction_text=f'Predicted Stock Price: {prediction[0]}')

# if __name__ == "__main__":
#     app.run(debug=True)
