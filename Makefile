install-tools:
	pip3 install pylint
	pip3 install mypy

lint:
	@pylint *.py

typecheck:
	@mypy .
