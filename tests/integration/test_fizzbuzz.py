import os

import pytest
from aiohttp import ClientSession

API_ENDPOINT = f"http://{os.environ['API_URL']}:{os.environ['API_PORT']}"
FIZZBUZZ_ENDPOINT = f"{API_ENDPOINT}/fizzbuzz"
STATISTICS_ENDPOINT = f"{API_ENDPOINT}/statistics"


@pytest.mark.asyncio
async def test_successful_fizzbuzz():
    fizzbuzz_data = {
        "factor1": 3,
        "factor2": 5,
        "limit": 15,
        "replacement1": "fizz",
        "replacement2": "buzz",
    }
    async with ClientSession() as session:
        response = await session.post(url=FIZZBUZZ_ENDPOINT, json=fizzbuzz_data)  # noqa
        assert response.status == 200
        response_json = await response.json()
        expected_response = [
            "1",
            "2",
            "fizz",
            "4",
            "buzz",
            "fizz",
            "7",
            "8",
            "fizz",
            "buzz",
            "11",
            "fizz",
            "13",
            "14",
            "fizzbuzz",
        ]
        assert response_json == expected_response


@pytest.mark.asyncio
async def test_fizzbuzz_missing_parameters():
    async with ClientSession() as session:
        # Missing factor1
        response = await session.post(
            url=FIZZBUZZ_ENDPOINT,
            json={
                "factor2": 5,
                "limit": 15,
                "replacement1": "fizz",
                "replacement2": "buzz",
            },
        )
        assert response.status == 422
        response_json = await response.json()
        assert "factor1" in response_json["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_fizzbuzz_limit_exceeds_maximum():
    fizzbuzz_data = {
        "factor1": 3,
        "factor2": 5,
        "limit": 101,  # Exceeding the allowed maximum which is 100
        "replacement1": "fizz",
        "replacement2": "buzz",
    }
    async with ClientSession() as session:
        response = await session.post(url=FIZZBUZZ_ENDPOINT, json=fizzbuzz_data)  # noqa
        assert response.status == 422  # 422 for validation errors in FastAPI
        response_json = await response.json()
        # Check if the error is specifically related to the 'limit' field
        assert "less than or equal to 100" in response_json["detail"][0]["msg"]


@pytest.mark.asyncio
async def test_statistics_endpoint():
    async with ClientSession() as session:
        # Making a few requests to /fizzbuzz
        fizzbuzz_data1 = {
            "factor1": 3,
            "factor2": 5,
            "limit": 15,
            "replacement1": "fizz",
            "replacement2": "buzz",
        }
        fizzbuzz_data2 = {
            "factor1": 4,
            "factor2": 6,
            "limit": 20,
            "replacement1": "fizz",
            "replacement2": "buzz",
        }
        await session.post(url=FIZZBUZZ_ENDPOINT, json=fizzbuzz_data1)
        await session.post(url=FIZZBUZZ_ENDPOINT, json=fizzbuzz_data1)
        await session.post(url=FIZZBUZZ_ENDPOINT, json=fizzbuzz_data2)
        # Fetching statistics
        response = await session.get(url=STATISTICS_ENDPOINT)
        assert response.status == 200
        response_json = await response.json()

        assert response_json["factor1"] == fizzbuzz_data1["factor1"]
        assert response_json["factor2"] == fizzbuzz_data1["factor2"]
        assert response_json["limit"] == fizzbuzz_data1["limit"]
        assert response_json["replacement1"] == fizzbuzz_data1["replacement1"]
        assert response_json["replacement2"] == fizzbuzz_data1["replacement2"]
        assert (
            response_json["count"] == 3
        )  # 3 because of the previous test request as well
