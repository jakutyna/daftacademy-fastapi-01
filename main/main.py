from hashlib import sha512

from fastapi import FastAPI, Request, Response

app = FastAPI()


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
        password_sha512 = sha512(password.encode('utf-8')).hexdigest()
        if password_sha512 == password_hash:
            response.status_code = 204
        else:
            response.status_code = 401
    return response.status_code
