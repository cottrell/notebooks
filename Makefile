all:
	cat ./Makefile

clean:
	./clean.sh yes

pull:
	./git_checkout_master_pull_all_submodules_parallel.sh

pull_slow:
	./git_checkout_master_pull_all_submodules.sh

push:
	./git_checkout_master_push_all_submodules_parallel.sh

push_slow:
	./git_checkout_master_push_all_submodules.sh

list:
	./git_list_submodules_recursive.sh
