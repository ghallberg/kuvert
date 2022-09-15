dev:
	pipenv run uvicorn kuvert:app --reload

migrate:
	pipenv run alembic upgrade head

lint:
	pipenv run black .
	pipenv run isort .
