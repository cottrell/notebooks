# Google AI Studio (Gemini Free Tier API)

Separate from your paid Antigravity (AGY) environment, Google offers a standalone free developer tier API.

## What To Try For Free

- **Provider**: Google (US).
- **Free Quota**: 15 requests/minute, 1,500 requests/day, 1M tokens/minute for free.
- **Key Signup**: [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (free Google account).

### Models To Test:
- `gemini-2.0-flash`: Extremely fast, 1M context window, strong reasoning & multimodal.

## Setup & Testing

```bash
export GEMINI_API_KEY="..."

# Test with aider:
aider --model gemini/gemini-2.0-flash
```

## CLI Installation

```bash
make install    # installs @google/gemini-cli via bun
make update
```
