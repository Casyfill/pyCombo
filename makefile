test:
	poetry install
	poetry run pytest tests/  --log-level DEBUG
