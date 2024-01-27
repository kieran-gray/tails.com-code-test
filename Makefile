PWD = $(shell pwd)
BUILD_POETRY_IMAGE = docker build --target builder -t package-installer .

install:
	docker compose build
	
run:
	docker compose up --force-recreate app

test: static-tests pytest

static-tests:
	docker compose run --no-deps test sh -c '\
	flake8 app && mypy app & black --check app && isort --check app'

pytest:
	docker compose run --rm --no-deps test sh -c 'pytest -vv --failed-first $(test)'

pytest-debug:
	PYTEST_OPTIONS="$(opt)" PYTEST_TEST="$(test)" docker compose up pytest-debug --build

format:
	docker compose run --rm --no-deps test sh -c 'black app && isort app'

add-package:
	$(BUILD_POETRY_IMAGE) && \
	docker run --rm -v $(PWD)/poetry.lock:/poetry.lock \
	-v $(PWD)/pyproject.toml:/pyproject.toml \
	package-installer sh -c 'poetry add --lock $(package) $(if $(group),"--group=$(group)",)'

remove-package:
	$(BUILD_POETRY_IMAGE) && \
	docker run --rm -v $(PWD)/poetry.lock:/poetry.lock \
	-v $(PWD)/pyproject.toml:/pyproject.toml \
	package-installer sh -c 'poetry remove --lock $(package) $(if $(group),"--group=$(group)",)' 

refresh-packages:
	$(BUILD_POETRY_IMAGE) && \
	docker run --rm -v $(PWD)/poetry.lock:/poetry.lock \
	-v $(PWD)/pyproject.toml:/pyproject.toml \
	package-installer sh -c 'poetry lock'