install-tools:
	pip3 install pylint
	pip3 install mypy
	pip3 install -r requirements.txt

lint:
	@pylint *.py

typecheck:
	@mypy .

test:
	@python3 -m unittest discover --verbose --start-directory tests --pattern *_tests.py
