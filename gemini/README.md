# Google AI Studio (Gemini Free Tier API)

Separate from your paid Antigravity (AGY) environment, Google offers a standalone free developer tier API.

## Free Quota

- **15 requests / minute**
- **1,500 requests / day**
- **1,000,000 tokens / minute**
- **Cost**: $0.00 (no billing account required).

## Key & Credential Setup

Your key is already stored in `~/.cred/ai.sh` as `GEMINI_API_KEY`.
To load it:
```bash
source ~/.cred/ai.sh
```

## Quick Commands & Usage

### 1. Test Connectivity
```bash
make test     # sends a curl ping to gemini-3.8-flash (returns 'pong')
```

### 2. Agentic Coding with `aider`
Use Gemini's massive 1M token context for free code edits in any git repo:
```bash
make aider    # runs: aider --model gemini/gemini-3.8-flash
```

### 3. Interactive TUI / Scratchpad with `aichat`
```bash
make aichat   # runs: aichat -m gemini:gemini-3.8-flash
```

### 4. Official Web UI (Browser)
If you prefer a web playground with huge prompt files, audio, and video uploads:
- URL: **[aistudio.google.com](https://aistudio.google.com/)**
- Sign in with your standard Google account.
- Free prompt prototyping with full access to Gemini models and system instructions.
