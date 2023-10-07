from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from .wsgi import application

app = FastAPI()


@app.get("/ping")
def ping():
    return {"message": "pong"}


app.mount("/", WSGIMiddleware(application))