# 2025-12-17

You're right to be skeptical — the configuration landscape has been shifting as Claude Code evolves.

Let me check the current documentation to give you an accurate answer:OK, now I have a clearer picture. You're absolutely right to be confused — this has been a moving target.

**The current official approach (replaces deprecated `ignorePatterns`):**

Put this in `~/.claude/settings.json` for global settings:

```json
{
  "permissions": {
    "deny": [
      "Read(.venv/**)",
      "Read(__pycache__/**)",
      "Read(node_modules/**)",
      "Read(.git/**)",
      "Read(*.pyc)"
    ]
  }
}
```

**The configuration hierarchy is:**
1. `~/.claude/settings.json` — global user settings
2. `.claude/settings.json` — project settings (checked into git)
3. `.claude/settings.local.json` — project-local settings (not checked in)

**What's deprecated/legacy:**
- `ignorePatterns` in settings.json — replaced by the `permissions.deny` approach with `Read()` patterns
- `~/.claude.json` — still exists but stores different things (OAuth, per-project state, caches)
- There's **no native `.claudeignore` file** — that's a third-party npm package (`claudeignore`) that uses hooks to achieve similar functionality

**The confusion sources:**
- Docs have lagged behind implementation
- Multiple GitHub issues note discrepancies between documentation and actual behavior
- Project-specific config handling has been buggy

So: `~/.claude/settings.json` with `permissions.deny` is your best bet for globals right now.

---

For global memory/instructions:

**`~/.claude/CLAUDE.md`** — global instructions that apply across all projects.

You can also have project-level ones:
- `CLAUDE.md` in project root
- `.claude/CLAUDE.md` in project

For agents:

**`~/.claude/agents/`** — global subagents available everywhere
**`.claude/agents/`** — project-specific subagents

So if you want global instructions that persist across all projects, create `~/.claude/CLAUDE.md` with your preferences, coding style, etc.

---

The agents in `~/.claude/agents/` are custom subagents you can invoke by name during a session.

Each agent is a markdown file with YAML frontmatter:

```markdown
# ~/.claude/agents/reviewer.md
---
name: reviewer
description: Code review specialist
tools:
  - Read
  - Glob
  - Grep
---

You are a code reviewer. Focus on:
- Security vulnerabilities
- Performance issues
- Code style consistency

Be terse. Flag only real problems.
```

Then you invoke it with:
```
/agent reviewer "review the auth module"
```

Or:
```
@reviewer review the auth module
```

So it's not "different instructions for the same Claude" — it's spawning a subagent with a constrained toolset and custom system prompt for a specific task. Useful for things like:

- `~/.claude/agents/test-writer.md`
- `~/.claude/agents/docs.md`
- `~/.claude/agents/refactor.md`

Each gets its own personality, tool permissions, and focus.
