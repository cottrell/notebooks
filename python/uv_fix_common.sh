#!/bin/bash
# once per (user) system. store first, so the uv update trusts the host.
sudo apt update && sudo apt install --only-upgrade ca-certificates || exit 1
UV_SYSTEM_CERTS=true uv self update || exit 1
uv --version
uv cache clean

# once per (user) system
uv python upgrade

# once per .venv ... see uv_fix_venvs.sh
command -v fdfind >/dev/null || sudo apt install fd-find || exit 1
fdfind -H -I -t d -g .venv ~/dev ~/projects ~/uv_venvs | tee venv-list.txt
./uv_fix_venvs.sh venv-list.txt
