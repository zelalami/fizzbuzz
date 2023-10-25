from fastapi import FastAPI

from .compute import compute_fizzbuzz
from .models import FizzBuzzParams

app = FastAPI()


@app.post("/fizzbuzz")
def fizzbuzz(params: FizzBuzzParams):
    result = compute_fizzbuzz(params)
    return result


@app.get("/statistics")
def statistics():
    pass
