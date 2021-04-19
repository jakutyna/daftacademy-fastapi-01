import pytest
from fastapi.testclient import TestClient
from main.main import app

client = TestClient(app)


def test_hello_world():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


def test_hello_world_online():
    response = client.get('https://da-plu-2021-jakutyna.herokuapp.com/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}

def test_method():
    response = client.get('/method')
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}
    response = client.put('/method')
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}
    response = client.options('/method')
    assert response.status_code == 200
    assert response.json() == {"method": "OPTIONS"}
    response = client.delete('/method')
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}
    response = client.post('/method')
    assert response.status_code == 201
    assert response.json() == {"method": "POST"}