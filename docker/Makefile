GAMES = snake tetris brick_breaker

all:
	for game in $(GAMES); do \
		bash docker/build_docker_image.sh $$game; \
	done

build:
	bash docker/build_docker_image.sh $(GAME)

test:
	bash docker/build_docker_image.sh $(GAME) --test-only
