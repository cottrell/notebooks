all:
	cat Makefile

build:
	cargo build --release

rust:
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

toolchain:
	@command -v rustup >/dev/null 2>&1 || $(MAKE) rust
	@rustc --version >/dev/null 2>&1 || $(MAKE) reinstall
	rustup default stable
	rustup update stable || $(MAKE) reinstall

reinstall:
	rustup toolchain uninstall stable || true
	rustup default stable

repair: reinstall

update: toolchain

install: rust toolchain
