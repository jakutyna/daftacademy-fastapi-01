from datetime import date, timedelta
from hashlib import sha512
from typing import Optional
import string

from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel

app = FastAPI()
app.id = 0
app.cache = []


# Ex1
@app.get('/')
def index_view():
    return {"message": "Hello world!"}


# Ex2
@app.api_route('/method', methods=["GET", "DELETE", "PUT", "OPTIONS"])
def method_view(request: Request):
    return {"method": request.method}


@app.post('/method', status_code=201)
def method_post_view():
    return {"method": "POST"}


# Ex3
@app.get('/auth')
def auth_view(response: Response,
              password: Optional[str] = None, password_hash: Optional[str] = None):
    if password is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response.status_code

    if '\\' in password:
        password_sha512 = sha512(r'{}'.format(password).encode('utf-8')).hexdigest()
    else:
        password_sha512 = sha512(password.encode('unicode-escape')).hexdigest()

    if password_sha512 == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    return response.status_code


# Ex4
class Register(BaseModel):
    name: str
    surname: str


def count_letters(word):
    alphabet = string.ascii_lowercase + string.ascii_uppercase
    return len([i for i in word if i in alphabet])


@app.post('/register', status_code=201)
def register_view(register: Register):
    app.id += 1
    today = date.today()
    days = count_letters(register.name) + count_letters(register.surname)
    output_json = {
        'id': app.id,
        'name': register.name,
        'surname': register.surname,
        'register_date': str(today),
        'vaccination_date': str(today + timedelta(days=days))
    }
    app.cache.append(output_json)
    return output_json


# Ex5
@app.get('/patient/{patient_id}')
def patient_view(patient_id: int, response: Response):
    if patient_id < 1:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response.status_code
    for patient_json in app.cache:
        if patient_json['id'] == patient_id:
            return patient_json
    response.status_code = status.HTTP_404_NOT_FOUND
    return response.status_code


# test auth

@app.get('/auth-test')
def auth_test_view(response: Response,
                   password: Optional[str] = None):
    if password is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response.status_code

    if '\\' in password:
        password_sha512 = sha512(r'{}'.format(password).encode('utf-8')).hexdigest()
    else:
        password_sha512 = sha512(password.encode('unicode-escape')).hexdigest()
    return password_sha512, password
