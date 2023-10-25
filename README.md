# fizzbuzz

This project implements the classic fizzbuzz algorithm as a RESTful API. Users can provide two integer factors, a limit, and two replacement strings. The API will return a list of strings with numbers from 1 to the limit, replacing multiples of the given factors with the provided strings.

## How to Run

1. Build and Start the service locally

```bash
make launch
```

Once the service is up and running, you can test it by sending a request to the fizzbuzz endpoint. Here's an example using curl:

```bash
curl -X POST "http://localhost:8000/fizzbuzz" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{"factor1": 3, "factor2": 5, "limit": 15, "replacement1": "fizz", "replacement2": "buzz"}'
```

2. Running integration tests

```bash
make test
```

## API Endpoints

1. **FizzBuzz computation**

   **Endpoint:** `/fizzbuzz`

   **Method:** `POST`

   **Payload:**

   ```json
   {
     "factor1": 3,
     "factor2": 5,
     "limit": 15,
     "replacement1": "fizz",
     "replacement2": "buzz"
   }
   ```

2. **Get the most frequent request**

   **Endpoint:** `/statistics`

   **Method:** `GET`

## Intructions for developers

- Ensure Docker and Docker-Compose are installed on your machine.
- This project uses pre-commit to ensure good code quality:
  - Ensure you have pre-commit installed. If not, you can install it with _pip install pre-commit_.
  - Run _pre-commit install_ to install the pre-commit hook.

## Future Enhancements

- Implement caching for improved performance with frequently-used parameters.
