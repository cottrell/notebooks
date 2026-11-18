all:
	cat Makefile

DEV_DIR := $(HOME)/dev/Backlog.md

install:
	bun i -g backlog.md

install-dev:
	@if [ -x "$(DEV_DIR)/dist/backlog" ]; then \
		ln -sfn "$(DEV_DIR)/dist/backlog" "$(HOME)/.bun/bin/backlog"; \
	else \
		echo "No compiled Backlog CLI at $(DEV_DIR)/dist/backlog; run 'make install' for the published CLI"; exit 1; \
	fi

update:
	@if [ -d "$(DEV_DIR)" ]; then \
		git -C $(DEV_DIR) pull && \
		$(MAKE) -C $(DEV_DIR) deps && \
		$(MAKE) -C $(DEV_DIR) install-dev; \
	else \
		bun i -g backlog.md@latest; \
	fi

