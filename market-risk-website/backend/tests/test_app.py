import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_collect_endpoint(client):
    test_data = {
        "feature1": 1.0,
        "feature2": 2.0,
        "risk_score": 0.5
    }
    response = client.post('/collect', json=test_data)
    assert response.status_code == 201
    assert b"Data stored successfully" in response.data

def test_predict_endpoint(client):
    test_data = {
        "feature1": 1.0,
        "feature2": 2.0
    }
    response = client.post('/predict', json=test_data)
    assert response.status_code in [200, 400]  # 400 if not enough training data 