# Mistral AI (La Plateforme)

French / EU frontier lab (GDPR compliant).

## What To Try For Free

Mistral provides a 100% free **"Experimenter" tier** on [La Plateforme](https://console.mistral.ai/) with rate-limited access.

### Key Model To Test: `codestral-latest`
- **What it is**: Mistral's dedicated 22B parameter model built specifically for coding.
- **Why try it**: 32k context, native fill-in-the-middle (FIM) support, great Python/JS/TS code generation.
- **Cost**: $0 on the Experimenter tier (no card needed).

## Setup & Testing

1. Get a free API key at **[console.mistral.ai/api-keys](https://console.mistral.ai/api-keys)**.
2. Set in your environment:
   ```bash
   export MISTRAL_API_KEY="..."
   ```
3. Test commands:
   ```bash
   make aider     # launches aider coding agent using codestral-latest
   make aichat    # launches aichat TUI using codestral-latest
   ```

## Installation (Mistral Vibe CLI)

```bash
make install   # installs mistral vibe CLI
make update
```
