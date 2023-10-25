import logging

from pymongo import MongoClient

from .models import FizzBuzzParams


class DBHelper:
    def __init__(self, logger: logging.Logger, host: str, port: int):
        self.logger = logger
        self.client = MongoClient(host, port)
        self.db = self.client["fizzbuzz_db"]
        self.requests_collection = self.db["requests"]

    def save_request(self, params: FizzBuzzParams):
        params_dict = params.model_dump()
        # check if a similar request already exists
        already_exists = self.requests_collection.find_one(params_dict)
        try:
            if already_exists:
                # increment the count
                self.requests_collection.update_one(
                    params_dict,
                    {"$inc": {"count": 1}},
                )
            else:
                params_dict["count"] = 1
                self.requests_collection.insert_one(params_dict)
        except Exception as e:
            self.logger.error(f"DBHELPER: Exception occured while save: {e}")

    def get_most_frequent_request(self):
        try:
            result = (
                self.requests_collection.find({}, {"_id": False})
                .sort("count", -1)
                .limit(1)
            )
            if result:
                return result[0]
            return None
        except Exception as e:
            self.logger.error(
                f"DBHELPER: Exception occured while finding "
                f"most recent request: {e}"
            )
            return None

    def close(self):
        if self.client:
            try:
                self.client.close()
            except Exception as e:
                self.logger.error(
                    f"DBHELPER: Exception occured while closing session: {e}"
                )
