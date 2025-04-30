from flask import Flask, request, jsonify
from pymongo import MongoClient
from database import Database
from model import RiskModel
import os
from dotenv import load_dotenv
import pandas as pd
from sklearn.linear_model import LinearRegression

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/market_risk")

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.market_risk
collection = db.risk_data

# Initialize database and model
database = Database(client)
model = RiskModel()

def train_regression_model():
    data = list(collection.find({}, {"_id": 0}))  # Fetch data, exclude MongoDB ID
    if len(data) < 2:
        return None  # Not enough data for regression
    
    df = pd.DataFrame(data)

    if "risk_score" not in df.columns:
        return None  # Target column missing

    X = df.drop(columns=["risk_score"])
    y = df["risk_score"]

    if X.empty or y.isnull().any():
        return None

    model = LinearRegression()
    model.fit(X, y)
    return model

@app.route("/collect", methods=["POST"])
def collect_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    collection.insert_one(data)
    return jsonify({"message": "Data stored successfully"}), 201

@app.route("/predict", methods=["POST"])
def predict_risk():
    model = train_regression_model()
    if not model:
        return jsonify({"error": "Not enough data to train model"}), 400
    
    input_data = request.json
    if not input_data:
        return jsonify({"error": "No input data provided"}), 400
    
    df = pd.DataFrame([input_data])

    # Ensure input matches trained model features
    expected_features = set(model.feature_names_in_)
    if set(df.columns) != expected_features:
        return jsonify({"error": "Invalid input features"}), 400
    
    prediction = model.predict(df)[0]
    return jsonify({"risk_score": round(prediction, 2)})

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    try:
        # Test MongoDB connection
        client.admin.command('ping')
        return jsonify({"status": "healthy", "mongodb": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route("/train", methods=["POST"])
def train():
    """Train model endpoint."""
    try:
        data = request.get_json()
        model.train(data)
        return jsonify({"status": "training completed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/data", methods=["GET"])
def get_data():
    """Get historical data endpoint."""
    try:
        data = database.get_historical_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
