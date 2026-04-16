all:
	cat Makefile

# --- Setup Targets ---
setup_all: setup_jax setup_pytorch setup_tf

setup_jax:
	./uv_setup_jax_env.sh

setup_pytorch:
	./uv_setup_pytorch_env.sh

setup_tf:
	./uv_setup_tf_env.sh

# --- Upgrade Targets ---
# Upgrades both external requirements and re-installs local editable packages
upgrade_all: upgrade_jax upgrade_pytorch upgrade_tf

upgrade_jax:
	./uv_upgrade_jax_env.sh
	$(MAKE) local_setup_jax

upgrade_pytorch:
	./uv_upgrade_pytorch_env.sh
	$(MAKE) local_setup_pytorch

upgrade_tf:
	./uv_upgrade_tf_env.sh
	$(MAKE) local_setup_tf

# --- Local Setup Targets (Per Env) ---
local_setup_all: local_setup_jax local_setup_pytorch local_setup_tf

local_setup_jax:
	bash -c ". $$HOME/uv_venvs/uv_3.12_jax/bin/activate && ./uv_local_setup.sh"

local_setup_pytorch:
	bash -c ". $$HOME/uv_venvs/uv_3.12_pytorch/bin/activate && ./uv_local_setup.sh"

local_setup_tf:
	bash -c ". $$HOME/uv_venvs/uv_3.12_tf/bin/activate && ./uv_local_setup.sh"

# --- Utilities ---
venv_reminder:
	@echo "To create a fresh venv with uv:"
	@echo "uv venv .venv --python 3.12"
	@echo "source .venv/bin/activate"
