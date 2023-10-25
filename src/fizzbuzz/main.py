import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .compute import compute_fizzbuzz
from .dbhelper import DBHelper
from .models import FizzBuzzParams

# Logger setup
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("api")


# Connect to db at startup and close connexion at shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect to mongodb
    app.db_helper = DBHelper(
        logger=logger,
        host=os.environ.get("MONGO_URL", "mongo"),
        port=int(os.environ.get("MONGO_PORT", 27017)),
    )
    yield
    # close connection
    app.db_helper.close()


app = FastAPI(lifespan=lifespan)


@app.post("/fizzbuzz")
def fizzbuzz(params: FizzBuzzParams):
    # save request to db for statistics purposes
    app.db_helper.save_request(params)
    result = compute_fizzbuzz(params)
    return result


@app.get("/statistics")
def statistics():
    most_frequent = app.db_helper.get_most_frequent_request()
    if most_frequent:
        return most_frequent
    return {"detail": "No data available"}
