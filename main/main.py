from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index_view():
    return {"message": "Hello world!"}
