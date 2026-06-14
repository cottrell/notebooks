HOST ?= ::
PORT ?= 47821

PIDFILE := /tmp/bifrost-gateway-$(PORT).pid
LOGFILE := /tmp/bifrost-gateway-$(PORT).log

.DEFAULT_GOAL := help

help:
	@echo "Bifrost Gateway (local dev on shared host)"
	@echo ""
	@echo "Quick:"
	@echo "  make gateway            foreground (test)"
	@echo "  make gateway-start      background (nohup + pid/log)"
	@echo ""
	@echo "Management:"
	@echo "  make gateway-status"
	@echo "  make gateway-stop"
	@echo "  make gateway-logs"
	@echo ""
	@echo "Persistence (recommended):"
	@echo "  make gateway-systemd-install"
	@echo "  # then run the printed 'systemctl --user' commands"
	@echo ""
	@echo "Other:"
	@echo "  make config             bifrost-cli"
	@echo ""
	@echo "Variables:"
	@echo "  HOST=:: PORT=47821      (override: make gateway-start PORT=12345)"
	@echo ""
	@echo "Notes:"
	@echo "  - First run downloads ~100MB binary (then cached)"
	@echo "  - Shared machine: use 'ps -p <pid>' before any kill"
	@echo "  - No Docker/K8s assumed here"
	@echo "  - See full targets below or 'cat Makefile'"

all:
	@cat Makefile

gateway:
	npx -y @maximhq/bifrost -host $(HOST) -port $(PORT)

# Persistent helpers below. See 'make help' for usage.

gateway-bg gateway-start:
	@rm -f $(PIDFILE) 2>/dev/null || true
	@echo "Launching Bifrost gateway in background on $(HOST):$(PORT)..."
	@nohup npx -y @maximhq/bifrost -host $(HOST) -port $(PORT) > $(LOGFILE) 2>&1 &
	@echo $$! > $(PIDFILE)
	@sleep 2
	@echo "PID file: $(PIDFILE)   (pid=$$(cat $(PIDFILE) 2>/dev/null || echo '?'))"
	@echo "Log file: $(LOGFILE)   (download + startup progress goes here)"
	@echo "Commands: make gateway-status | make gateway-stop | make gateway-logs"

gateway-stop:
	@echo "Stopping tracked pid (ps -p first)..."
	-@if [ -f $(PIDFILE) ]; then \
		PID=$$(cat $(PIDFILE) 2>/dev/null || true); \
		if [ -n "$$PID" ] && ps -p $$PID >/dev/null 2>&1; then \
			kill $$PID 2>/dev/null || true; \
			sleep 1; \
			if ps -p $$PID >/dev/null 2>&1; then kill -9 $$PID 2>/dev/null || true; fi; \
		fi; \
		rm -f $(PIDFILE); \
	fi
	-@pkill -f 'npx.*@maximhq/bifrost.*$(PORT)' 2>/dev/null || true
	-@pkill -f 'bifrost-http.*$(PORT)' 2>/dev/null || true
	@echo "Stop attempted. Re-check with: make gateway-status"

gateway-status:
	@echo "=== Bifrost gateway status (port $(PORT)) ==="; \
	if [ -f $(PIDFILE) ]; then \
		PID=$$(cat $(PIDFILE) 2>/dev/null || true); \
		if [ -n "$$PID" ] && ps -p $$PID >/dev/null 2>&1; then \
			echo "Running (tracked pid=$$PID)"; \
			ps -p $$PID -o pid,ppid,etime,cmd; \
		else \
			echo "Pidfile present but pid not alive (stale)."; \
			rm -f $(PIDFILE); \
		fi; \
	else \
		echo "No pidfile."; \
	fi; \
	echo "Sockets:"; \
	ss -tlnp 2>/dev/null | grep :$(PORT) || echo "  (not listening)"; \
	echo "Visible procs:"; \
	ps aux | grep -E '[n]px.*bifrost|[b]ifrost-http' | grep -v grep || echo "  (none)"

gateway-logs:
	@tail -n 30 -f $(LOGFILE) 2>/dev/null || echo "No log yet. Start the gateway first."

# systemd user service (recommended). Run 'make gateway-systemd-install' then follow printed steps.
# (see 'make help' for summary)
gateway-systemd-install:
	@mkdir -p $(HOME)/.config/systemd/user
	@printf '[Unit]\nDescription=Bifrost AI Gateway\nAfter=network-online.target\nWants=network-online.target\n\n[Service]\nType=simple\nEnvironment=PATH=$(HOME)/.nvm/versions/node/current/bin:$(HOME)/.nvm/versions/node/v25.2.1/bin:$(HOME)/.bun/bin:/usr/local/bin:/usr/bin:/bin\nExecStart=/usr/bin/env npx -y @maximhq/bifrost -host $(HOST) -port $(PORT)\nRestart=on-failure\nRestartSec=5\nStandardOutput=journal\nStandardError=journal\nSyslogIdentifier=bifrost-gateway\n\n[Install]\nWantedBy=default.target\n' > $(HOME)/.config/systemd/user/bifrost-gateway.service
	@echo "Wrote $(HOME)/.config/systemd/user/bifrost-gateway.service"
	@echo ""
	@echo "Run these (in your shell):"
	@echo "  systemctl --user daemon-reload"
	@echo "  systemctl --user enable bifrost-gateway.service"
	@echo "  systemctl --user start bifrost-gateway.service"
	@echo "  systemctl --user status bifrost-gateway.service"
	@echo ""
	@echo "Logs (live):   journalctl --user -u bifrost-gateway.service -f"
	@echo "Stop:          systemctl --user stop bifrost-gateway.service"
	@echo "Disable:       systemctl --user disable bifrost-gateway.service"
	@echo ""
	@echo "To change HOST/PORT: edit the Makefile vars, re-run 'make gateway-systemd-install', then 'systemctl --user daemon-reload && systemctl --user restart bifrost-gateway.service'"
	@echo "Confirm any stop with: ps -p <pid> first."

config:
	bunx @maximhq/bifrost-cli

