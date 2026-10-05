all:
	cat Makefile

build:
	cargo build --release

rust:
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

toolchain:
	rustup update stable

update: toolchain

install: rust toolchain
