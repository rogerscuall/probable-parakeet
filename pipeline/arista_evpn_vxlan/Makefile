# Run from the generated project root, with avd/ and pipeline/.
.DEFAULT_GOAL := help
.PHONY: help init install validate build build-all

UV ?= uv
PYTHON ?= 3.12
INVENTORY ?= avd/inventory.yml
FABRIC ?= FABRIC
export ANSIBLE_CONFIG := $(CURDIR)/pipeline/ansible.cfg
export ANSIBLE_COLLECTIONS_PATH := $(CURDIR)/.ansible/collections

# Generated locally so the published bundle needs no additional manifest files.
# uv add creates .venv and uv.lock; no shell activation is needed.
UV_RUN = $(UV) run --python "$(PYTHON)"

help:
	@echo "init       Initialize a local uv project (requires uv)"
	@echo "install    Create .venv and install Python and Ansible dependencies"
	@echo "validate   Validate inventory, AVD inputs, and playbook syntax"
	@echo "build      Validate and generate EOS configurations and documentation"
	@echo "build-all  Alias for build"
	@echo "Overrides: UV=uv PYTHON=3.12 INVENTORY=avd/inventory.yml FABRIC=FABRIC"

init:
	@if [ ! -f pyproject.toml ]; then \
		$(UV) init --bare --no-workspace --vcs none --python "$(PYTHON)"; \
	fi

install: init
	$(UV) add --python "$(PYTHON)" -r pipeline/requirements.txt
	$(UV_RUN) ansible-galaxy collection install -r pipeline/requirements.yml -p "$(ANSIBLE_COLLECTIONS_PATH)"

validate:
	$(UV_RUN) python pipeline/scripts/validate_avd.py "$(INVENTORY)" --fabric "$(FABRIC)"
	$(UV_RUN) ansible-playbook -i "$(INVENTORY)" pipeline/build.yml -e "fabric_name=$(FABRIC)" --syntax-check

build: validate
	$(UV_RUN) ansible-playbook -i "$(INVENTORY)" pipeline/build.yml -e "fabric_name=$(FABRIC)"

build-all: build