all:
	cat Makefile

install: install_from_gh

install_from_gh:
	./install_latest_from_gh.sh

install_using_system_packager:
	./install_using_system_packager.sh

clean:
	dl syncthing*

restart:
	pkill syncthing || :
	syncthing > $(HOME)/logs/syncthing_`/bin/date +\%Y-\%m-\%dT\%H:\%M:\%S`.log 2>&1 &
