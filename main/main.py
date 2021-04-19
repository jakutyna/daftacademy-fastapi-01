from datetime import date, timedelta
from hashlib import sha512

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

app = FastAPI()
app.id = 0


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
def auth_view(response: Response, password: str = None, password_hash: str = None):
    if password is None:
        response.status_code = 401
    else:
        password_sha512 = sha512(password.encode('unicode-escape')).hexdigest()
        if password_sha512 == password_hash:
            response.status_code = 204
        else:
            response.status_code = 401
    return response.status_code


# Ex4
class Register(BaseModel):
    name: str
    surname: str


@app.post('/register', status_code=201)
def register_view(register: Register):
    app.id += 1
    today = date.today()
    days = len(register.name) + len(register.surname) + 5
    output_json = {
        'id': app.id,
        'name': register.name,
        'surname': register.surname,
        'register_date': str(today),
        'vaccination_date': str(today + timedelta(days=days))
    }
    return output_json
