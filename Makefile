dev:
	pipenv run uvicorn kuvert:app --reload

lint:
	pipenv run black .
	pipenv run isort
