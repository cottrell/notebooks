all:
	cat Makefile

serve:
	docsify serve docs

serve_lan:
	# did not find a way to listen via doscify serve
	cd docs && live-server --host=0.0.0.0 --port=3333

install:
	bun i docsify-cli -g

init:
	docsify init ./docs
