from fastapi.testclient import TestClient
from src.app import app

def test_predict_requires_file():
    client = TestClient(app)
    r = client.post("/predict")
    assert r.status_code in (400, 422)