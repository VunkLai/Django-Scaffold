pipeline: format lint test

format:
	black server --check --diff
	isort server --check-only --diff

lint:
	pylint server/*
	mypy server/

test:
	poetry run python server/manage.py check
	pytest server

requirements:
	poetry export -f requirements.txt --output requirements.txt

init:
	poetry run python server/manage.py migrate
	poetry run python server/manage.py runserver
