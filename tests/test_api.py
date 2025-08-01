from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_index_get():
    response = client.get("/")
    
    assert response.status_code == 200

def test_index_post_data():
    response = client.post("/", data={"data": "test_data"})
    
    assert response.status_code == 200
    assert "test_data" in response.text

def test_index_post_cap_string():
    response = client.post("/", data={"cap_string": "test_cap_string"})
    
    assert response.status_code == 200
    assert "test_cap_string" in response.text

def test_index_post_data_and_cap_string():
    response = client.post("/", data={"data": "test_data", "cap_string": "test_cap_string"})
    
    assert response.status_code == 200
    assert "test_data" in response.text
    assert "test_cap_string" in response.text