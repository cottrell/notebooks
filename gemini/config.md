# 2025-12-27

For the Gemini CLI, all global configuration lives in the **`~/.gemini/`** directory in your home folder.

Unlike Claude, which uses `AGENTS.md`, Gemini CLI follows a specific naming convention for instructions and handles ignores through its settings or dedicated files.

### 1\. Global Instructions (System Prompt)

To give Gemini instructions that apply to **every** project and session:

  * **Primary Location:** `~/.gemini/GEMINI.md`
  * **Alternative Location:** `~/.gemini/instructions.md`

> **Note:** By default, Gemini CLI looks for `GEMINI.md`. If you want it to look for a different filename (like `instructions.md` or `GLOBAL.md`), you can configure this in your `settings.json` (see below).

-----

### 2\. Global Ignore Files

Gemini CLI does not have a single `~/.geminiignore` file that it checks by default for every project. Instead, it handles "ignoring" in two ways:

  * **Respecting Git:** It automatically respects your project's `.gitignore`.
  * **The `.aiexclude` / `.geminiignore` file:** While these are usually **project-level** files, you can simulate a global ignore by pointing the CLI to a central exclusion file in your global settings.

-----

### 3\. How to Set it Up (Configuration)

To verify or change where Gemini looks for these files, edit your global settings file:
**Path:** `~/.gemini/settings.json`

```json
{
  "context": {
    "fileName": ["GEMINI.md", "instructions.md"],
    "loadMemoryFromIncludeDirectories": true
  },
  "fileFiltering": {
    "respectGitIgnore": true
  }
}
```

### Quick Summary Table

| Config Type | Global Path (CLI) |
| :--- | :--- |
| **Global Folder** | `~/.gemini/` |
| **Global Instructions** | `~/.gemini/GEMINI.md` |
| **Global Settings** | `~/.gemini/settings.json` |
| **Global Ignores** | Managed via `.gitignore` or project-level `.geminiignore` |

**Would you like me to show you how to set up a `GEMINI_SYSTEM_MD` environment variable to point to a single custom instruction file anywhere on your system?**

---

To set up **global** instructions and ignores for the Gemini CLI (not using `.gitignore`), you use the `~/.gemini/` directory.

### 1\. Global Instructions

Unlike Claude's `~/.claude/AGENTS.md`, Gemini looks for a Markdown file at this specific path:

  * **Global Path:** `~/.gemini/GEMINI.md`
  * **Alternative Path:** `~/.gemini/instructions.md` (Supported by some versions, but `GEMINI.md` is the official standard for the CLI).

**How it works:**
The CLI searches for `GEMINI.md` starting from your current project directory and moves up the tree. If it doesn't find one in the project, it falls back to the one in your home folder (`~/.gemini/GEMINI.md`).

-----

### 2\. Global Ignore (Files to Exclude)

Gemini CLI does not look for a `~/.geminiignore` file by default. However, you can enforce a **global ignore** by using the `settings.json` file.

**Step 1: Open/Create the settings file**
Path: `~/.gemini/settings.json`

**Step 2: Add `fileFiltering` and `includeDirectories`**
To ignore specific patterns globally without using `.gitignore`, configure the `fileFiltering` block:

```json
{
  "fileFiltering": {
    "respectGitIgnore": true,
    "ignorePatterns": [
      "**/secret_folder/**",
      "*.log",
      "personal_notes.md",
      "custom_exclude_pattern/*"
    ]
  }
}
```

  * **`ignorePatterns`**: This is your global "ignore list." It uses glob syntax (like `.gitignore`) but lives inside your global config.
  * **`respectGitIgnore`**: If you set this to `false`, Gemini will **only** use your `ignorePatterns` and ignore your project's `.gitignore` entirely.

-----

### 3\. Summary of Global CLI Paths

| Feature | Path |
| :--- | :--- |
| **Global Directory** | `~/.gemini/` |
| **Instructions** | `~/.gemini/GEMINI.md` |
| **Ignore Patterns** | `~/.gemini/settings.json` (under `ignorePatterns`) |
| **Custom Commands** | `~/.gemini/commands/` |

**Would you like me to help you write a `GEMINI.md` with specific rules for your coding style?**

---

• I set a clink override so Gemini runs with working_dir set to this repo:

  - ~/.pal/cli_clients/gemini.json now includes:
      - "working_dir": "/home/cottrell/dev/council-data"

