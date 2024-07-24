.PHONY: req sync

req:
	uv pip compile pyproject.toml -o requirements/base.txt > /dev/null
	uv pip compile --extra dev pyproject.toml -o requirements/dev.txt > /dev/null

makemigrations:
	docker compose run app python src/manage.py makemigrations

migrate:
	docker compose run app python src/manage.py migrate
