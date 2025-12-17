# 2025-12-17

**TL;DR:** *As of late-2025 there is **no built-in “global ignore” mechanism** in OpenAI’s Codex CLI comparable to a `.gitignore` or the ignorePatterns proposals — it **doesn’t support global file/dir ignore patterns** in `~/.codex/config.toml` or a `.codexignore` file yet. The relevant GitHub issues request this feature but it isn’t implemented.* ([GitHub][1])

---

## Current reality (late 2025)

**1) No official ignore/glob exclude support**

* Codex CLI lacks documented config for ignoring files globally.
* GitHub issues explicitly request **global and project ignore patterns** and `.codexignore`, but these are **feature requests**, not shipped features. ([GitHub][1])

**2) What config *does* do**

* `~/.codex/config.toml` exists and configures things like default model, sandbox, approval policy, environment filtering, profiles, etc. — but **no ignorePatterns key is supported** in official docs. ([OpenAI Developers][2])
* CLI flags (`--config key=value`) override parts of `config.toml` ad-hoc, but again **no ignore config** surfaces. ([docs.onlinetool.cc][3])

**3) AGENTS.md / global guidance**

* Codex uses `~/.codex/AGENTS.md` or `AGENTS.override.md` to define persistent instructions, but it is *guidance*, not an ignore/exclusion mechanism. ([OpenAI Developers][4])

**4) Workarounds**

* There is no official pattern-based ignore; the common workaround pattern is:

  * **sandbox_level** and strict **approval_policy** to limit Codex actions on dangerous files.
  * Manipulate environment (`shell_environment_policy`) to prevent leaking sensitive env vars. ([OpenAI Developers][2])

---

## Example – What people *wish* global ignore would look like (discussed only in request issues)

**Proposed in issues (not implemented):**

```jsonc
// ~/.codex/config.json (hypothetical)
{
  "ignorePatterns": [
    "**/.env",
    "**/*.pem",
    "secrets/**",
    "config/*.yml"
  ]
}
```

or a `.codexignore` file like:

```
# Secrets
.env
*.pem
secrets/
```

**These are *requests* — not functional features yet.** ([GitHub][5])

---

## Practical summary

* **There is no built-in global ignore** in Codex CLI that will stop it from scanning/reading files based on globs.
* `~/.codex/config.toml` does *not* support ignore patterns as of current CLI versions.
* Ignore functionality appears on *feature request* issues, not in released code.
* Your best controls for sensitive content today are sandbox/approval policies and careful directory scoping, not ignore/glob patterns.

---

If you want, I can draft a *snippet for a proposed `.codexignore` + wrapper enforcement* using OS-level hooks (e.g., symlink sandbox directories or drive mounts to limit Codex visibility) that works around this limitation.

[1]: https://github.com/openai/codex/issues/2847?utm_source=chatgpt.com "A way to exclude sensitive files · Issue #2847 · openai/codex · GitHub"
[2]: https://developers.openai.com/codex/local-config?utm_source=chatgpt.com "Configuring Codex"
[3]: https://docs.onlinetool.cc/codex/docs/config.html?utm_source=chatgpt.com "Config · Codex Docs"
[4]: https://developers.openai.com/codex/guides/agents-md/?utm_source=chatgpt.com "Custom instructions with AGENTS.md"
[5]: https://github.com/openai/codex/issues/1397?utm_source=chatgpt.com "Configurable file exclusion patterns for sensitive files · Issue #1397 · openai/codex · GitHub"


---


Short answer:

* **Yes, Codex uses `AGENTS.md`.**
* **No, there is no `CODEX.md`.**
* **No, there is no `.codex/agents/` hierarchy like Claude.**

Details.

---

## Codex instruction files (actual, current)

### 1. Project-local

```
./AGENTS.md
```

* Canonical, documented.
* Read automatically by Codex CLI.
* Applies to the entire repo.
* This is the *only* project-level instruction file Codex looks for.

---

### 2. Global (user-level)

```
~/.codex/AGENTS.md
```

* Optional.
* Acts as a global preamble across all repos.
* Merged with project `AGENTS.md` (global first, project overrides).

---

### 3. Override (hard override, not merged)

```
~/.codex/AGENTS.override.md
```

* Replaces all other AGENTS instructions.
* Useful for temporary hard constraints.

---

## What Codex does **not** have

### ❌ No `.codex/agents/AGENTS.md`

* Claude Code supports per-agent instruction directories.
* Codex does **not** have agent-scoped instruction files.
* Codex is effectively **single-agent + profiles**, not agent trees.

### ❌ No `CODEX.md`

* Never existed.
* Not read.
* Any mention of `CODEX.md` is hallucination or confusion with `README.md`.

### ❌ No per-subdirectory instruction files

* Codex does not recurse looking for AGENTS files.
* Only the repo root matters.

---

## Mental model (important)

Codex instruction resolution:

[
\text{Instructions}
===================

\begin{cases}
\texttt{AGENTS.override.md}, & \text{if exists} \
\texttt{~/.codex/AGENTS.md} ;\oplus; \texttt{./AGENTS.md}, & \text{otherwise}
\end{cases}
]

No agent graph. No hierarchy. No per-tool instructions.

---

## Practical implication (vs Claude)

If you want Claude-style multi-agent behavior in Codex:

* You must **simulate agents in text** (roles, prefixes).
* Or orchestrate externally (your Python subprocess coordinator).
* Codex itself will not manage agent-scoped memory or instruction files.

---

If you want, I can give you:

* A **minimal AGENTS.md template** tuned for Codex CLI
* Or a **Codex-vs-Claude parity map** showing exactly what must be emulated externally

Just say which.

