# Groq Cloud

Ultra-fast hosted inference running on custom LPU silicon (250–500 tok/s). 

## Free Tier Overview

- **Provider**: Groq, Inc. (Mountain View, CA, USA — US commercial jurisdiction).
- **Free Quota**: ~30 RPM, 14,400 requests/day. 100% free with no credit card required.
- **Key Signup**: [console.groq.com/keys](https://console.groq.com/keys)

## Hosted Free Models

- `llama-3.3-70b-versatile`: General architecture and reasoning (Meta weights)
- `qwen-2.5-coder-32b`: Strong dedicated coding model (Alibaba open weights on US LPU hardware)
- `deepseek-r1-distill-llama-70b`: Reasoning model with chain-of-thought traces

## Installation & CLI

```bash
make install    # installs groq-cli as 'grc' via uv tool
make update
make uninstall
```

## Quick Commands

Set your key first:
```bash
export GROQ_API_KEY="gsk_..."
```

Run test or launch agents:
```bash
make test             # verify API connection via curl
make aider-llama      # run aider coding agent with Llama 3.3 70B
make aider-qwen       # run aider coding agent with Qwen 2.5 Coder
make aider-reasoning  # run aider with DeepSeek R1 reasoning distill
```
