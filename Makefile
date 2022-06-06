install-tools:
	pip3 install pylint
	pip3 install mypy
	pip3 install requests
	pip3 install types-requests

lint:
	@pylint *.py

typecheck:
	@mypy .

test:
	@python3 -m unittest discover --verbose --start-directory tests --pattern *_tests.py
