# 2025-12-17

https://docs.mistral.ai/mistral-vibe/introduction/configuration

... seems like nothing is implicit, no defaults in mistral. YOu have to select an agent to use a prompt.

NOTE: seems like .vibe/instructions.md is legacy

---

Yes — **Mistral Vibe has its own global and per-agent config structure, but it is *different*** from Claude/Codex AGENTS.md style.

Here’s what official docs show:

### 1) No `.vibe/AGENTS.md` by default

Vibe does **not** use a single global AGENTS.md instruction file like Claude/Codex. It uses `config.toml` plus *prompts* and *agent config files* instead. ([Mistral AI][1])

### 2) Config locations

Vibe config hierarchy (defaults):

```
./.vibe/config.toml    ← project-local
~/.vibe/config.toml    ← global fallback
```

Plus:

```
~/.vibe/.env           ← API keys
~/.vibe/prompts/       ← custom system prompts
~/.vibe/agents/        ← custom agent definitions
```

Agents under `~/.vibe/agents/` are **TOML config files**, not markdown instruction files. ([Mistral AI][1])

### 3) How global instructions work

**System prompts** in `~/.vibe/prompts/*.md` approximate “instructions”:

* A file like `~/.vibe/prompts/my_custom_prompt.md` can define a system default.
* You select it via `system_prompt_id` in config. ([Mistral AI][1])

Example:

```toml
system_prompt_id = "my_custom_prompt"
```

Then Vibe loads `~/.vibe/prompts/my_custom_prompt.md`. ([Mistral AI][1])

### 4) Agent configs in `~/.vibe/agents/`

These are TOML files like:

```
~/.vibe/agents/redteam.toml
```

They define model and tool permissions for *named agents* you can launch with `vibe --agent redteam`. ([Mistral AI][1])

This is **not a Markdown AGENTS.md** — it’s structured config.

### 5) No fallback to markdown instruction file for global rules

Unlike Codex/Claude where `~/.codex/AGENTS.md` or `~/.claude/CLAUDE.md` is read and merged, Vibe:

* Loads `config.toml`
* Uses the named `system_prompt_id` to pick a prompt file
* Loads `~/.vibe/agents/*.toml` only if you select an agent

There’s *no built-in `.vibe/AGENTS.md` convention* for global instructions. Behavior is driven via prompts and agent config files. ([Mistral AI][1])

---

## Rough hierarchy summary

```
~/.vibe/config.toml       ← global config
~/.vibe/.env              ← API keys
~/.vibe/prompts/*.md      ← global system prompts
~/.vibe/agents/*.toml     ← named agent configs
./.vibe/config.toml       ← project override
```

No `.vibe/AGENTS.md` by default, and no global instruction markdown unless you *invent your own system prompt*.

---

## Practical conclusion

If your goal is *global consistent behavior* in Vibe:

* Don’t use AGENTS.md like you do for Codex/Claude
* Instead use:

  * A **custom prompt Markdown in `~/.vibe/prompts/`**
  * Reference it via `system_prompt_id` in your `config.toml`

That gives you a **portable, tool-agnostic instruction base** aligned with Vibe’s design. ([Mistral AI][1])

---

If you want a *template for Vibe system prompts* that mirrors your Codex/Claude AGENTS.md semantics, tell me and I’ll generate one.

[1]: https://docs.mistral.ai/mistral-vibe/introduction/configuration?utm_source=chatgpt.com "Configuration | Mistral Docs"

1

---

Correct. In **Vibe nothing is implicit**. A prompt file does nothing until it is **named and selected in config.toml**.

There is **no automatic “default AGENTS.md” equivalent**.

---

## Mental model (important)

Vibe separates:

* **Config** → *what to load*
* **Prompt** → *what the agent is told*
* **Agent** → *which model/tools*

If you don’t wire them together, nothing happens.

---

## How to get a *default* global agent behavior

### Step 1 — create the prompt

Put your instructions here:

```
~/.vibe/prompts/default.md
```

Example (your AGENTS content works fine verbatim):

```md
YOU MUST NOT read or modify .venv/ or node_modules/ unless explicitly instructed.
Prefer minimal diffs. Avoid refactors unless requested.
Use uv for Python. Prefer DuckDB.
```

This file is inert by itself.

---

### Step 2 — select it in global config

Edit:

```
~/.vibe/config.toml
```

Add **at top level**:

```toml
system_prompt_id = "default"
```

That’s the key line.

What this means:

[
\text{system prompt} \leftarrow ~/.vibe/prompts/default.md
]

Now **every invocation** that does not override the system prompt will use it.

---

## That’s it — you now have a “default agent”

No need for:

* `~/.vibe/agents/*.toml`
* named agents
* per-project config

You are using the **unnamed default agent**, but with a fixed system prompt.

---

## Precedence (so you’re not surprised later)

Order of resolution:

1. CLI flags (highest)
2. Project `./.vibe/config.toml`
3. Global `~/.vibe/config.toml`
4. Prompt referenced by `system_prompt_id`
5. Built-in default (only if you didn’t set one)

So if later you add:

```
./.vibe/config.toml
```

with another `system_prompt_id`, it will override the global one.

---

## What Vibe does *not* have (important)

* ❌ No auto-loaded `.vibe/AGENTS.md`
* ❌ No implicit “default prompt”
* ❌ No merging of multiple prompt files

Exactly **one system prompt** is active at a time.

---

## Recommendation for your setup

Given how you work:

* Keep **one global prompt**: `~/.vibe/prompts/default.md`
* Set it once in `~/.vibe/config.toml`
* Do *not* bother with named agents unless you want different tool permissions

This gives you parity with:

* `~/.codex/AGENTS.md`
* `~/.claude/CLAUDE.md`

If you want, I can:

* Translate your final AGENTS.md → **Vibe-optimized prompt**
* Or give you a **side-by-side Codex / Claude / Vibe mapping table**

