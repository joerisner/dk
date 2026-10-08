.DEFAULT_GOAL=help
.PHONY: build clean help install lint setup

build: ## Build the package
	@uv build

clean: ## Remove temporary artifacts
	@bin/clean

install: ## Install dependencies and update the environment
	@uv sync

lint: ## Run lint and format checks
	@uv run ruff check

setup: ## Setup the project
	@bin/setup

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; \
	printf "\nCommands:\n\033[35m\033[0m"} /^[$$()% a-zA-Z_-]+:.*?##/ { \
	printf "  \033[35;1m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { \
	printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
