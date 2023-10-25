.PHONY: launch

DC_LOCAL_FILE=docker-compose.yaml

# Launch the app locally
launch:
	docker-compose -f $(DC_LOCAL_FILE) down && docker-compose -f $(DC_LOCAL_FILE) up --build
