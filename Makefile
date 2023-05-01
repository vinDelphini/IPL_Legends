
clean:
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "__pycache__" -delete

update_requirements:
	pip install -U -q pip-tools
	pip-compile --output-file=requirements/base.txt requirements/base.in

install_requirements:
	@echo 'Installing pip-tools...'
	export PIP_REQUIRE_VIRTUALENV=true; \
	pip install -U -q pip-tools
	@echo 'Installing requirements...'
	pip-sync requirements/base.txt

setup:
	@echo 'Setting up the environment...'
	make install_requirements

run-dev:
	@echo 'Running local development'
	python3 manage.py runserver

run-tests:
	@echo 'Checking for migrations'
	python manage.py makemigrations --dry-run --check
	pytest

shutdown:
	@echo 'Shutting down servers'
	sudo pkill -f runserver
	