format:
	ruff format .

lint:
	ruff check .
	mypy .

lint-fix:
	ruff check --fix .

test:
	pytest tests/

test-cov:
	pytest --cov=./lib tests/

build:
	poetry build

publish:
	poetry publish
