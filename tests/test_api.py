from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_index_get():
    response = client.get("/")
    
    assert response.status_code == 200

def test_index_post():
    response = client.post("/")
    
    assert response.status_code == 200