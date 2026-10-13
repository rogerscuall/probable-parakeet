# Run from the generated project root, alongside inventory.yml and group_vars/.
.DEFAULT_GOAL := help
.PHONY: help install validate build build-all

PYTHON ?= python3
INVENTORY ?= inventory.yml
FABRIC ?= FABRIC
export ANSIBLE_CONFIG := $(CURDIR)/ansible.cfg

help:
	@echo "install    Install Python and Ansible collection dependencies"
	@echo "validate   Validate inventory, AVD inputs, and playbook syntax"
	@echo "build      Validate and generate EOS configurations and documentation"
	@echo "build-all  Alias for build"
	@echo "Overrides: PYTHON=python3 INVENTORY=inventory.yml FABRIC=FABRIC"

install:
	$(PYTHON) -m pip install -r requirements.txt
	ansible-galaxy collection install -r requirements.yml

validate:
	$(PYTHON) scripts/validate_avd.py "$(INVENTORY)" --fabric "$(FABRIC)"
	ansible-playbook -i "$(INVENTORY)" build.yml -e "fabric_name=$(FABRIC)" --syntax-check

build: validate
	ansible-playbook -i "$(INVENTORY)" build.yml -e "fabric_name=$(FABRIC)"

build-all: build
