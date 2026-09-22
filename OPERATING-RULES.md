# fundcfo — operating rules

Ground rules every fundcfo skill follows. This file is the single source of truth. After editing it, run `python3 scripts/sync-operating-rules.py` from the repo root to copy the current text into every skill, between its `<!-- OPERATING-RULES:START -->` / `<!-- OPERATING-RULES:END -->` markers. Each skill carries its own copy because each must work standalone — a skill can't assume another skill's file was read this session, so the rules can't live in just one place. Edit only this file; the copies inside `skills/*/SKILL.md` are generated and get overwritten.

Everything from the `## Ground rules` heading down is what gets copied. Keep it self-contained: it has to make sense dropped into any skill, with no other section for context.

## Ground rules

### Files and memory

Two kinds of memory. **Solid**: files in the session's working folder (the Cowork Project folder, or in Claude Code the launch directory), in fixed formats, meant to persist and be trusted. **Fluid**: the chat itself and Cowork's native memory. Never the only place something lives — if losing it would be a problem, it goes in a file.

Plugin-owned files, at the root of the working folder:

- `todos.md` — the task list.
- `actions.md` — a high-level history of what the plugin has done. Not a technical run log.
- `config.yaml` — user preferences.

Write these freely, without asking for confirmation. Never write inside the plugin's own install directory, which is replaced on every update. User-owned files (the reports, spreadsheets and other documents the user brought) are different: read them freely, but see "Asking before acting" below before changing one.

### First run in a folder

`todos.md` and `actions.md` are created together, on whichever comes first: the first task or the first logged action. Their presence is the setup signal:

- **Neither exists:** first run in this folder. Say so plainly instead of guessing.
- **Both exist:** normal.
- **Only one exists:** flag it in one line — name the missing file and the folder you're in — before continuing. It means a file was moved or deleted, or the user is in a different folder than usual.

### Status line

Before anything else, every entry point opens with exactly one line stating where things stand: what this folder is set up for (`config.yaml`'s `fund_name` if set, otherwise the folder name), the open task counts from `todos.md`, and when `actions.md` last changed. On a first run, say so instead of showing counts: "First run in this folder — no tasks yet, nothing logged." Any deviation from what the user expects should be obvious from this one line alone. Keep it to one line — this is meant to be the recognizable opening of this tool, not a status dump.

### actions.md

Append-only; never overwrite or reorder. One line per meaningful action — something that changed state, not every file read or every reply:

`<timestamp> | <what happened>`

Log: a task added, changed or dropped; a document reviewed (with a short result); a config change; a file written outside the routine plugin-owned files; anything outward-facing, such as a message sent. Don't log file reads, or a chat answer that changed nothing. Get the timestamp from `date -u +%Y-%m-%dT%H:%M:%SZ` at the time of the action; never guess it.

Examples:

```
2026-09-22T10:15:00Z | Added task "Send Q3 LP report"
2026-09-22T10:20:00Z | Reviewed Q2-draft.pdf: 3 findings, 1 note
2026-09-22T10:21:00Z | Marked task "Send Q3 LP report" as Done
```

A future version may add a separate, technical run-by-run log; if it ever exists, it also lives in the working folder, never in the plugin's install directory. Not built now — `actions.md` is the only log.

### Tasks

- Add a task to `todos.md` as soon as the user states one; don't wait to be asked to save it.
- Never delete a task line. Change its status to `Dropped` instead, so the history stays intact.
- Don't change a task's status unless the user asked about that task. Don't mark things done on inference.
- Log every add, status change and edit as one `actions.md` line.
- If `todos.md` has lines that don't match the format, keep every such line exactly as it is, salvage what you can from lines that are close (for example a missing field), and tell the user which lines you couldn't parse and what you did. Never drop or overwrite a task silently.

### Asking before acting

- **Never ask:** reading files in the working folder; writing or updating the plugin-owned files above.
- **Ask first:** modifying, renaming, moving or deleting a user-owned document; anything outside the working folder; anything outward-facing (email, Slack, payments, once those exist); resetting or overwriting a plugin-owned file beyond its normal append or update.
- **Ask once, then proceed:** an ambiguous input, for example which file is the draft. Don't ask again for the same ambiguity within one run.

### References and highlights

A skill can hold a `references/` folder, one file per task it supports (for example `do-reporting/references/review.md`). The skill's own `SKILL.md` stays short: it names its tasks and says which are live. A reference file can mark itself `highlight: true` in its front matter with a one-line `try:` prompt; the `/fundcfo` entry point's Menu surfaces every highlighted, live reference this way, under option 1. A reference with no `highlight` is still usable, just not surfaced.
