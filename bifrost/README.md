# bifrost

High-performance AI gateway ([maximhq/bifrost](https://github.com/maximhq/bifrost)) routing multiple LLM providers through a single OpenAI-compatible endpoint.

## Architecture

```
agents (claude, codex, gemini, grok, vibe)
        │
        ▼
http://bleepblop:47821  ← bifrost gateway (binds ::, yggdrasil-accessible)
        │
        ├── /anthropic  → Anthropic API
        ├── /openai     → OpenAI API
        ├── /gemini     → Google Gemini
        ├── /xai        → xAI (Grok)
        └── /groq       → Groq
```

## Quick start

```bash
make gateway          # start gateway on :: port 8080
make config           # run interactive wizard to patch an agent
```

Override host/port:

```bash
make gateway HOST=:: PORT=47821
```

## Provider config — `~/.bifrost/config.json`

```json
{
  "$schema": "https://www.getbifrost.ai/schema",
  "providers": {
    "anthropic": {
      "keys": [{ "name": "primary", "value": "env.ANTHROPIC_API_KEY", "models": ["*"], "weight": 1.0 }]
    },
    "openai": {
      "keys": [{ "name": "primary", "value": "env.OPENAI_API_KEY", "models": ["*"], "weight": 1.0 }]
    },
    "gemini": {
      "keys": [{ "name": "primary", "value": "env.GEMINI_API_KEY", "models": ["*"], "weight": 1.0 }]
    },
    "xai": {
      "keys": [{ "name": "primary", "value": "env.XAI_API_KEY", "models": ["*"], "weight": 1.0 }]
    },
    "groq": {
      "keys": [{ "name": "primary", "value": "env.GROQ_API_KEY", "models": ["*"], "weight": 1.0 }]
    }
  }
}
```

`"env.VAR"` reads from your shell environment — set keys in `.bashrc`/`.zshrc`.

## Per-agent setup

Run `make config` and select the agent. The wizard patches each agent automatically.

| Agent | Transport | How bifrost patches it |
|---|---|---|
| Claude Code | `/anthropic` | sets `ANTHROPIC_BASE_URL=http://bleepblop:47821/anthropic` |
| Codex CLI | `/openai` | sets `OPENAI_BASE_URL=http://bleepblop:47821/openai/v1` |
| Gemini CLI | `/genai` | sets `GOOGLE_GEMINI_BASE_URL`, passes `-m provider/model` |
| Opencode | `/openai` | generates runtime config |

### Grok / Vibe (manual — not in wizard yet)

Point them at the OpenAI-compatible endpoint:

```bash
export OPENAI_BASE_URL="http://bleepblop:47821/openai/v1"
export OPENAI_API_KEY="bifrost"   # placeholder; bifrost uses the real key
```

Then use model strings like `xai/grok-3` or `groq/llama-3.3-70b-versatile`.

## LAN / Yggdrasil access

Gateway binds to `::` (all IPv6 interfaces) by default, so any machine on the
yggdrasil network can reach it at `http://bleepblop:47821`.

Point remote agents at `http://bleepblop:8080` instead of `localhost`.

## Web UI

`http://bleepblop:47821` — provider key management, routing rules, usage dashboard.

## Model targeting syntax

```
provider/model-name
```

Examples:

```
anthropic/claude-sonnet-4-6
openai/gpt-4o
gemini/gemini-2.5-pro
xai/grok-3
groq/llama-3.3-70b-versatile
```
