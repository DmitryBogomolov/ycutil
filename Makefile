install-tools:
	pip3 install pylint
	pip3 install mypy
	pip3 install types-requests

lint:
	@pylint *.py

typecheck:
	@mypy .
