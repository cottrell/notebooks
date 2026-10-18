# OpenRouter Free Pool

Unified API router providing access to a zero-dollar pool of open models tagged with `:free`.

## Free Tier Overview

- **Provider**: OpenRouter, Inc. (Delaware / Remote, USA).
- **Free Quota**: ~20 req/min, 200 req/day on `:free` endpoints. Zero deposit or credit card required.
- **Key Signup**: [openrouter.ai/keys](https://openrouter.ai/keys)

## Free Model Catalog

OpenRouter routes to models hosted and sponsored by third-party GPU clouds. Current live `:free` models include:
- `google/gemma-4-31b-it:free`
- `cohere/north-mini-code:free` (code-specialized)
- `deepseek/deepseek-r1:free` (671B reasoning model)
- `meta-llama/llama-3.3-70b-instruct:free`
- `nvidia/nemotron-3.5-lightning:free`

Inspect live free models anytime:
```bash
make list-free
```

## Installation & CLI

```bash
make install    # installs openrouter-cli via bun
make update
make uninstall
```

## Quick Commands

Set your key:
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

Run test or coding agent:
```bash
make test         # tests API connection
make aider-r1     # run aider coding agent with DeepSeek R1 free endpoint
make aider-llama  # run aider coding agent with Llama 3.3 70B free endpoint
```
