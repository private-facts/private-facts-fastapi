from fastapi.testclient import TestClient
import pytest

from api.main import app, get_tahoe_client


client = TestClient(app)


class FakeTahoe:
    """
    An object which mocks a Tahoe client.
    """
    def __init__(self, storage={}, bad_response=False):
        self.storage = storage
        self.bad_response = bad_response
        self.fake_data = {
            'test_data': 'test_cap_string'
        }


    def post_data(self, data, exception=False):
        if exception:
            raise ValueError("Simulated exception.")
        if self.bad_response:
            return None
        cap_string = self.fake_data.get(data) # Get the URI from the fake_data dict
        self.storage[cap_string] = data # Store the URI as key and the data as value for later retrieval
        return cap_string

    def get_data(self, cap_string):
        if self.bad_response:
            status = 400
            return None, status
        status = 200
        return self.storage.get(cap_string), status


def test_index_get_happy():
    response = client.get("/")
    
    assert response.status_code == 200
    assert "Private facts demo" in response.text
    assert "Here you can try out the Tahoe-LAFS public test grid" in response.text
    assert "Input text" in response.text
    assert "Input capability string" in response.text
    assert "test_data" not in response.text
    assert "test_cap_string" not in response.text

def test_index_post_data_happy():
    fake_tahoe = FakeTahoe()
    app.dependency_overrides[get_tahoe_client] = lambda: fake_tahoe

    response = client.post("/", data={"data": "test_data"})

    assert response.status_code == 200
    assert "test_cap_string" in response.text
    assert "test_data" not in response.text

def test_index_post_cap_string_happy():
    fake_tahoe = FakeTahoe()
    app.dependency_overrides[get_tahoe_client] = lambda: fake_tahoe

    response = client.post("/", data={"cap_string": "test_cap_string"})

    assert response.status_code == 200
    assert "test_data" in response.text
    assert "test_cap_string" not in response.text

def test_index_post_no_data_or_cap_string():
    fake_tahoe = FakeTahoe()
    app.dependency_overrides[get_tahoe_client] = lambda: fake_tahoe

    response = client.post("/")

    assert response.status_code == 200
    assert "test_data" not in response.text
    assert "test_cap_string" not in response.text