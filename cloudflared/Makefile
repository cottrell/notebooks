# cloudflared on bleepblop (Grok Voice MCP)
# Account: Proton / govlakia (NOT gmail). Tunnel: desktop-mcp (dashboard).
# Token lives in /etc/cloudflared/token — do not commit, do not paste.
# 127.0.0.1 in the CF UI is this desktop, not the laptop.
#
# Install (apt). Disable leftover focal client list if apt 404s:
#   sudo mv /etc/apt/sources.list.d/cloudflare-client.list \
#     /etc/apt/sources.list.d/cloudflare-client.list.disabled
# Then dashboard's:
#   sudo mkdir -p --mode=0755 /usr/share/keyrings
#   curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg \
#     | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
#   echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' \
#     | sudo tee /etc/apt/sources.list.d/cloudflared.list
#   sudo apt-get update && sudo apt-get install cloudflared
#   sudo cloudflared service install   # token from Proton Tunnels UI
#
# Grok connector URL = Public hostname in Tunnels UI + /mcp
#   https://mcp.govlakia.org/mcp   (or .com / .co.uk — whichever zone you attached)
#
# Origin: http://127.0.0.1:13001  (desktop-mcp). Not Workers.

BINARY := ./cloudflared
MCP ?= http://127.0.0.1:13001

.PHONY: all help install status logs quick clean

all:
	@cat Makefile

help:
	@echo "make install  - download ./cloudflared (fallback; apt is canonical)"
	@echo "make status   - systemd cloudflared"
	@echo "make logs     - journalctl -u cloudflared"
	@echo "make quick    - one-off trycloudflare (dies on exit; not Grok keep-it)"

install: $(BINARY)

$(BINARY):
	curl -L -o $(BINARY) https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
	chmod +x $(BINARY)

status:
	systemctl is-active cloudflared
	systemctl status cloudflared --no-pager -n 20

logs:
	journalctl -u cloudflared -f

quick: install
	$(BINARY) tunnel --url $(MCP)

clean:
	rm -f $(BINARY)
