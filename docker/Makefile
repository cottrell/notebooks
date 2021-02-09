all:
	cat Makefile

prune_container:
	docker container prune --filter "until=168h"

prune_image:
	docker image prune -a --filter "until=168h"

prune:
	docker image prune -a --filter "until=168h"
	docker system prune -a -f

