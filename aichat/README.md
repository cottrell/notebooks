# aichat

Fast, lightweight Rust terminal TUI and REPL for multi-provider LLM chat.

## Installation

```bash
make install    # pulls x86_64 static musl binary to ~/.local/bin/aichat
make update     # updates to latest GitHub release
make uninstall
```

## How It Works

`aichat` is an agent client / harness — it does not run models itself. It routes prompts to hosted API providers configured in `~/.config/aichat/config.yaml`.

## Quick Start (Free Tiers)

1. Grab a free API key from **[Groq Cloud](https://console.groq.com/keys)** (free, no credit card required).
2. Set it in your environment:
   ```bash
   export GROQ_API_KEY="gsk_..."
   ```
3. Test or launch the interactive TUI:
   ```bash
   make query-groq    # one-off test
   make repl          # interactive TUI
   ```

## Pre-Configured Endpoints in Makefile

- `make query-groq`: runs `llama-3.3-70b-versatile` on Groq Cloud
- `make query-mistral`: runs `codestral-latest` on Mistral (requires `MISTRAL_API_KEY`)
