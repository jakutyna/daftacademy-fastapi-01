from fastapi import FastAPI, Request

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
