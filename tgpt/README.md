# tgpt

Zero-configuration terminal AI client. Works out-of-the-box with **no API keys, no accounts, and no payment required**.

## Installation

```bash
make install    # installs to ~/.local/bin/tgpt
make update     # checks remote version and only updates if newer release exists
make uninstall
```

## Quick Commands

```bash
make test          # runs: tgpt --provider pollinations "reply pong in one word"
make interactive   # launches interactive TUI mode (no keys needed)
make test-img      # generates an image to /tmp/tgpt_test.jpg
```

## Direct Shell Usage

```bash
# Simple scratchpad query:
tgpt --provider pollinations "Explain this bash one-liner"

# Pipe input:
cat file.py | tgpt --provider pollinations "Refactor this function"
```

## How It Works

Routes anonymously to community/open-source free model endpoints (Pollinations.ai in Berlin, Germany under EU GDPR). No local GPU or account tracking required.
