all:
	cat ./Makefile

clean:
	./clean.sh yes

git_clean:
	./git_clean.sh

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

list_submodules:
	./list_submodules.sh

status:
	git submodule status
	git config --local --get-regexp submodule\..*\.active


fsck:
	git submodule foreach --recursive 'echo Checking $$name; git fsck --full; git lfs fsck --objects;'
