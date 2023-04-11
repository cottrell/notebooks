all:
	cat ./Makefile

clean:
	./clean.sh yes

pull:
	./git_checkout_master_pull_all_submodules.sh

push:
	./git_checkout_master_push_all_submodules.sh
