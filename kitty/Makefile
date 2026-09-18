all:
	cat Makefile

install:
	curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin
	mkdir -p ~/.local/bin
	ln -sf ~/.local/kitty.app/bin/kitty ~/.local/kitty.app/bin/kitten ~/.local/bin/
	cp ~/.local/kitty.app/share/applications/kitty.desktop ~/.local/share/applications/

config:
	./setup.sh
