from pymongo import MongoClient
import pandas as pd
from sklearn.linear_model import LinearRegression
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["risk_db"]
collection = db["application_data"]

class RiskModel:
    """Market risk prediction model."""
    
    def __init__(self):
        """Initialize the model."""
        self.model = LinearRegression()
        self.is_trained = False
    
    def train(self, data):
        """Train the model with historical data."""
        try:
            df = pd.DataFrame(data)
            X = df[['market_volatility', 'trading_volume', 'price_momentum']]
            y = df['risk_score']
            self.model.fit(X, y)
            self.is_trained = True
        except Exception as e:
            raise Exception(f"Training failed: {str(e)}")
    
    def predict(self, data):
        """Predict market risk for new data."""
        if not self.is_trained:
            raise Exception("Model not trained yet")
        try:
            df = pd.DataFrame([data])
            X = df[['market_volatility', 'trading_volume', 'price_momentum']]
            prediction = self.model.predict(X)
            return float(prediction[0])
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")

def train_regression_model():
    data = list(collection.find({}, {"_id": 0}))  # Fetch data, exclude MongoDB ID
    if len(data) < 2:
        return None  # Not enough data for regression
    
    df = pd.DataFrame(data)
    
    if "risk_score" not in df.columns:
        return None  # Target column missing

    X = df.drop(columns=["risk_score"])  # Features
    y = df["risk_score"]  # Target

    if X.empty or y.isnull().any():
        return None  # Ensure valid training data

    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_risk(input_data):
    model = train_regression_model()
    if not model:
        return None
    
    df = pd.DataFrame([input_data])
    
    # Ensure input columns match training features
    if set(df.columns) != set(model.feature_names_in_):
        return None
    
    prediction = model.predict(df)[0]
    return prediction
