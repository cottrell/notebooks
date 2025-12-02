all:
	cat Makefile

build:
	cargo build --release

rust:
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

toolchain:
	rustup toolchain uninstall stable
	rustup toolchain install stable

install: rust toolchain
