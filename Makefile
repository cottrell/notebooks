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

update-agy:
	cd antigravity && $(MAKE) update

update-gemini:
	cd gemini && $(MAKE) update

update-codex:
	cd codex && $(MAKE) update

update-mistral:
	cd mistral && $(MAKE) update

update-claude:
	cd claude && $(MAKE) update

update-grok:
	cd grok && $(MAKE) update

update-ai: update-claude update-codex update-agy update-grok
	cd agentsview && $(MAKE) update
	# cd copilot && $(MAKE) update
	# cd kimi && $(MAKE) update
	# cd qwen && $(MAKE) update
	cd tgpt && $(MAKE) update
	cd aichat && $(MAKE) update
	cd aider && $(MAKE) update

update:               ## System‑wide update (APT + snap + AI tools)
	# 1️⃣ keep sudo alive for the whole recipe
	sudo -v
	# 2️⃣ regular Debian/Ubuntu packages
	sudo apt update && sudo apt upgrade -y
	# 3️⃣ **new** snap packages (including Firefox)
	$(MAKE) snap-update
	# 4️⃣ AI‑related sub‑projects (unchanged from before)
	$(MAKE) update-ai
	# 5️⃣ language‑runtime toolchains (unchanged)
	cd rust && make toolchain
	cd bun && $(MAKE) update

	cd backlogmd && $(MAKE) update
	# cd typst && $(MAKE) update
	cd gh && $(MAKE) update
	# cd nodejs && $(MAKE) update
	cd python && $(MAKE) upgrade_jax
	cd python && $(MAKE) upgrade_pytorch

snap-update:            ## Refresh all snap packages (Firefox included)
	# Snap refresh runs as root; `sudo` is required
	sudo snap refresh
