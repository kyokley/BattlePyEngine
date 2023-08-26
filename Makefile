.PHONY: autoformat tests

autoformat: build-dev
	git ls-files | grep -P '\.py$$' | xargs docker run --rm -t -v $$(pwd):/code/BattlePyEngine kyokley/battlepyengine /venv/bin/isort
	git ls-files | grep -P '\.py$$' | xargs docker run --rm -t -v $$(pwd):/code/BattlePyEngine kyokley/battlepyengine /venv/bin/black -S

tests: build-dev
	docker run --rm -it -v $$(pwd):/code/BattlePyEngine kyokley/battlepyengine /venv/bin/pytest
	git ls-files | grep -E '\.py$$' | xargs docker run --rm -t -v $$(pwd):/code/BattlePyEngine kyokley/battlepyengine /venv/bin/black -S --check

build:
	docker build -t kyokley/battlepyengine --target=base .

build-dev:
	docker build -t kyokley/battlepyengine --target=dev .

shell:
	docker run --rm -it -v $$(pwd):/code/BattlePyEngine kyokley/battlepyengine /bin/bash

