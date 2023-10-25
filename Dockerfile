# Base layer with shared setup
FROM python:3.11-slim as base
WORKDIR /app

# Copy requirements file and the source code
COPY requirements/ requirements/
COPY src/ .


# Application layer
FROM base as fizzbuzz-app
RUN pip install --no-cache-dir -r requirements/requirements.txt
EXPOSE 8000
CMD ["uvicorn", "fizzbuzz.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Test layer
FROM base as tests
COPY tests/ ./tests/
RUN pip install --no-cache-dir -r requirements/tests_requirements.txt
