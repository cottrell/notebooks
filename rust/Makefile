all:
	cat Makefile

build:
	cargo build --release

install:
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

toolchain:
	rustup toolchain uninstall stable
	rustup toolchain install stable

