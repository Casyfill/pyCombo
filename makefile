test:
	uv sync
	uv run pytest tests/ --log-level DEBUG
