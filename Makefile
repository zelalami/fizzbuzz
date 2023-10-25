.PHONY: tests-up tests-down test launch

# Name of the test docker-compose file
DC_TEST_FILE=tests/integration/docker-compose.yaml
# Name of the local docker-compose file
DC_LOCAL_FILE=docker-compose.yaml

# Start tests services
tests-up:
	docker-compose -f $(DC_TEST_FILE) up --build -d
# Stop tests services
tests-down:
	docker-compose -f $(DC_TEST_FILE) down

# Run integration tests
test: tests-up
	docker-compose -f $(DC_TEST_FILE) logs -f tests
	make tests-down

# Launch the app locally
launch:
	docker-compose -f $(DC_LOCAL_FILE) down && docker-compose -f $(DC_LOCAL_FILE) up --build
