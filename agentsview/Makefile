all:
	cat Makefile

install:
	# https://www.agentsview.io/quickstart/
	curl -fsSL https://agentsview.io/install.sh | bash

update:
	agentsview update

HOST ?= ::
PORT ?= 8080

serve start:
	agentsview serve --host '$(HOST)' --port $(PORT) --no-browser
