all:
	cat Makefile

DEV_DIR := $(HOME)/dev/Backlog.md

install:
	bun i -g backlog.md

install-dev:
	@if [ -d "$(DEV_DIR)" ]; then \
		$(MAKE) -C $(DEV_DIR) install-dev; \
	else \
		echo "Dev directory $(DEV_DIR) not found"; exit 1; \
	fi

update:
	@if [ -d "$(DEV_DIR)" ]; then \
		$(MAKE) -C $(DEV_DIR) install-dev; \
	else \
		bun i -g backlog.md@latest; \
	fi

