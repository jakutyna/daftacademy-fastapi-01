from datetime import date, timedelta
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


def test_auth():
    response = client.get(
        '/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215')
    assert response.status_code == 204
    assert response.text == '204'
    response = client.get(
        '/auth?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091')
    assert response.status_code == 401
    assert response.text == '401'
    response = client.get('/auth')
    assert response.status_code == 401
    assert response.text == '401'


def test_register():
    response = client.post('/register', json={"name": "Jan", "surname": "Nowacki"})
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Jan",
        "surname": "Nowacki",
        "register_date": str(date.today()),
        "vaccination_date": str(date.today() + timedelta(days=10))
    }
    response = client.post('/register', json={"name": "Jan Sebastian", "surname": "Bach"})
    assert response.status_code == 201
    assert response.json() == {
        "id": 2,
        "name": "Jan Sebastian",
        "surname": "Bach",
        "register_date": str(date.today()),
        "vaccination_date": str(date.today() + timedelta(days=16))
    }


def test_patient():
    response = client.post('/register', json={"name": "Jan", "surname": "Nowacki"})
    assert response.status_code == 201
    response = client.post('/register', json={"name": "Jan Sebastian", "surname": "Bach"})
    assert response.status_code == 201
    response = client.get('/patient/1')
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Jan",
        "surname": "Nowacki",
        "register_date": str(date.today()),
        "vaccination_date": str(date.today() + timedelta(days=10))
    }
    response = client.get('/patient/2')
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "name": "Jan Sebastian",
        "surname": "Bach",
        "register_date": str(date.today()),
        "vaccination_date": str(date.today() + timedelta(days=16))
    }
    response = client.get('/patient/3')
    assert response.status_code == 404
    response = client.get('/patient/-1')
    assert response.status_code == 400
