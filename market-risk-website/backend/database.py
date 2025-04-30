from pymongo import MongoClient
import os
from dotenv import load_dotenv


class Database:
    """Database handler for market risk data."""
    
    def __init__(self):
        """Initialize database connection."""
        load_dotenv()
        self.client = MongoClient(os.getenv('MONGO_URI'))
        self.db = self.client["risk_db"]
        self.collection = self.db["application_data"]
    
    def get_historical_data(self):
        """Get all historical market data."""
        try:
            data = list(self.collection.find({}, {"_id": 0}))
            return data
        except Exception as e:
            raise Exception(f"Failed to fetch data: {str(e)}")
    
    def insert_data(self, data):
        """Insert new market data."""
        try:
            self.collection.insert_one(data)
            return True
        except Exception as e:
            raise Exception(f"Failed to insert data: {str(e)}")
