# Use games.json dynamically
ROOT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))../)
GAMES := $(shell jq -r '.games[]' $(ROOT_DIR)/games.json)

.PHONY: all build test no-test

# Build Docker image for all games
all:
	@for game in $(GAMES); do \
		echo "🛠️ Building $$game..."; \
		bash $(ROOT_DIR)/docker/build_docker_image.sh $$game; \
	done

# Build a specific game via: make build GAME=snake
build:
	@bash $(ROOT_DIR)/docker/build_docker_image.sh $(GAME)

# Test-only build via: make test GAME=tetris
test:
	@bash $(ROOT_DIR)/docker/build_docker_image.sh $(GAME) --test-only

# Build without test: make no-test GAME=snake
no-test:
	@bash $(ROOT_DIR)/docker/build_docker_image.sh $(GAME) --no-test
