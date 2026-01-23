# AWS CloudWAN Pipeline - Local Makefile
# ======================================
#
# ASSUMPTIONS:
# ------------
# 1. Terraform is installed locally (tested with v1.6.0+)
# 2. UV (Python package manager) is installed locally
# 3. AWS credentials are configured (via env vars or AWS CLI)
# 4. .env file exists in this directory with required variables
#
# REQUIRED .env VARIABLES:
# ------------------------
# AWS_DEFAULT_REGION=us-east-1
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
#
# USAGE:
# ------
# make validate          - Validate design data
# make generate-policy   - Generate policy JSON
# make generate-terraform - Generate Terraform files
# make plan              - Run terraform plan
# make apply             - Run terraform apply (requires plan)
# make build-all         - Run full pipeline (validate → generate → plan)
# make deploy-all        - Run full pipeline including apply
#

.PHONY: help validate generate-policy generate-terraform generate-all plan apply build-all deploy-all clean check-env

# Load environment variables from .env file
ifneq (,$(wildcard .env))
    include .env
    export
endif

# Default variables (can be overridden by .env)
AWS_DEFAULT_REGION ?= us-east-1
TF_DIR := terraform
DATA_DIR := data

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo ""
	@echo "$(CYAN)AWS CloudWAN Pipeline - Local Makefile$(NC)"
	@echo "========================================"
	@echo ""
	@echo "$(YELLOW)Assumptions:$(NC)"
	@echo "  • Terraform is installed locally (v1.6.0+)"
	@echo "  • UV (Python package manager) is installed"
	@echo "  • AWS credentials configured via .env or AWS CLI"
	@echo "  • .env file exists with required variables"
	@echo ""
	@echo "$(YELLOW)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

check-env: ## Verify required tools and environment
	@echo "$(CYAN)Checking environment...$(NC)"
	@command -v terraform >/dev/null 2>&1 || { echo "$(RED)Error: terraform is not installed$(NC)"; exit 1; }
	@command -v uv >/dev/null 2>&1 || { echo "$(RED)Error: uv is not installed$(NC)"; exit 1; }
	@echo "  ✓ Terraform: $$(terraform version -json | grep -o '"terraform_version":"[^"]*"' | cut -d'"' -f4)"
	@echo "  ✓ UV: $$(uv --version)"
	@if [ -f .env ]; then echo "  ✓ .env file found"; else echo "$(YELLOW)  ⚠ .env file not found (using defaults)$(NC)"; fi
	@echo "  ✓ AWS_DEFAULT_REGION: $(AWS_DEFAULT_REGION)"
	@echo "$(GREEN)Environment check passed$(NC)"
	@echo ""

# =============================================================================
# STAGE: validate
# =============================================================================

validate: check-env ## Validate design data files
	@echo "$(CYAN)[validate] Running data validation...$(NC)"
	uv run python pipeline/scripts/validate.py $(DATA_DIR)/
	@echo "$(GREEN)[validate] Validation completed$(NC)"
	@echo ""

# =============================================================================
# STAGE: generate
# =============================================================================

generate-terraform: check-env ## Generate Terraform files from design data
	@echo "$(CYAN)[generate-terraform] Generating Terraform files...$(NC)"
	uv run python pipeline/scripts/generate_terraform.py $(DATA_DIR)/ --output $(TF_DIR)/
	@echo "$(GREEN)[generate-terraform] Terraform files generated in: $(TF_DIR)/$(NC)"
	@echo ""

generate-policy: check-env generate-terraform ## Generate policy JSON from design data
	@echo "$(CYAN)[generate-policy] Generating policy.json...$(NC)"
	uv run python pipeline/scripts/generate_policy.py $(DATA_DIR)/ --output $(TF_DIR)/policy.json
	@echo "$(GREEN)[generate-policy] Policy generated: $(TF_DIR)/policy.json$(NC)"
	@echo ""

generate-all: generate-terraform generate-policy ## Run all generate tasks
	@echo "$(GREEN)[generate] All generation tasks completed$(NC)"
	@echo ""

# =============================================================================
# STAGE: plan
# =============================================================================

plan: check-env ## Run terraform init and plan
	@echo "$(CYAN)[plan] Initializing Terraform...$(NC)"
	cd $(TF_DIR) && terraform init
	@echo ""
	@echo "$(CYAN)[plan] Running Terraform plan...$(NC)"
	cd $(TF_DIR) && terraform plan -out=tfplan
	@echo "$(GREEN)[plan] Plan saved to: $(TF_DIR)/tfplan$(NC)"
	@echo ""

# =============================================================================
# STAGE: apply
# =============================================================================

apply: check-env ## Run terraform apply (requires existing plan)
	@echo "$(CYAN)[apply] Applying Terraform plan...$(NC)"
	@if [ ! -f $(TF_DIR)/tfplan ]; then \
		echo "$(RED)Error: tfplan not found. Run 'make plan' first.$(NC)"; \
		exit 1; \
	fi
	cd $(TF_DIR) && terraform init && terraform apply -auto-approve tfplan
	@echo "$(GREEN)[apply] Terraform apply completed$(NC)"
	@echo ""

# =============================================================================
# COMBINED TARGETS
# =============================================================================

build-all: validate generate-all plan ## Run full pipeline: validate → generate → plan
	@echo ""
	@echo "$(GREEN)========================================$(NC)"
	@echo "$(GREEN)Build pipeline completed successfully!$(NC)"
	@echo "$(GREEN)========================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Next step:$(NC) Run 'make apply' to deploy to AWS"
	@echo ""

deploy-all: build-all apply ## Run full pipeline including apply
	@echo ""
	@echo "$(GREEN)========================================$(NC)"
	@echo "$(GREEN)Full deployment completed successfully!$(NC)"
	@echo "$(GREEN)========================================$(NC)"
	@echo ""

# =============================================================================
# UTILITY TARGETS
# =============================================================================

clean: ## Clean generated files
	@echo "$(CYAN)Cleaning generated files...$(NC)"
	rm -f $(TF_DIR)/policy.json
	rm -f $(TF_DIR)/tfplan
	rm -f $(TF_DIR)/*.tfstate*
	rm -rf $(TF_DIR)/.terraform
	@echo "$(GREEN)Clean completed$(NC)"
	@echo ""

init: check-env ## Initialize Terraform only
	@echo "$(CYAN)[init] Initializing Terraform...$(NC)"
	cd $(TF_DIR) && terraform init
	@echo "$(GREEN)[init] Terraform initialized$(NC)"
	@echo ""

fmt: ## Format Terraform files
	@echo "$(CYAN)[fmt] Formatting Terraform files...$(NC)"
	cd $(TF_DIR) && terraform fmt -recursive
	@echo "$(GREEN)[fmt] Formatting completed$(NC)"
	@echo ""

destroy: check-env ## Destroy Terraform infrastructure (DANGEROUS)
	@echo "$(RED)WARNING: This will destroy all managed infrastructure!$(NC)"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	cd $(TF_DIR) && terraform destroy
	@echo "$(GREEN)[destroy] Infrastructure destroyed$(NC)"
	@echo ""
