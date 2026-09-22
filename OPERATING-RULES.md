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

- **Neither exists:** first run in this folder. Run the folder connection check below. If it found a clear signal to warn about, lead with that; otherwise open plainly with: "Looks like this is the first time FundCFO is running in this folder — where should we start?" This is the one place a longer opening is fine; it happens once.
- **Both exist:** normal — see Status line.
- **Only one exists:** flag it in one line — name the missing file and the folder you're in — before continuing. It means a file was moved or deleted, or the user is in a different folder than usual.

Alongside `todos.md`/`actions.md`, on a genuine first run also write a pointer file, `CLAUDE.md`, at the folder root — skip this if one already exists there, don't overwrite a file you didn't create:

```
This folder is managed by the fundcfo plugin. Task list: todos.md. History: actions.md.
If the user asks about their tasks, a report review, or other fund-CFO work in this folder,
tell them to type `/fundcfo` to get started. Don't act on the request yourself without that.
```

Plugin-owned files always stay in the folder they were first created in. Granting access to more folders later (for reading comparison sources, say) never changes where `todos.md`, `actions.md` or `config.yaml` get written. If you expect them and don't find them in the current folder, check other connected folders before treating it as a fresh first run — say what you found, and use that location, rather than silently starting a second set elsewhere.

#### Folder connection check

Persistence depends on a real, connected folder, and there's no confirmed way to know from inside a skill whether one exists — it may vary by host. Before writing `todos.md`/`actions.md` for the first time, look at whatever your own context tells you about where that write will land. Only act on a clear signal: if what you can see plainly indicates non-persistent, temporary or account-level storage rather than a real folder on the user's machine, say so and tell them to connect a local folder before relying on anything from this session. If you can't tell either way — no clear signal, or a path that looks like an ordinary folder — say nothing about it and proceed as an ordinary first run. Don't ask the user to go check anything themselves; a warning on a guess is worse than no warning.

This is deliberately quiet on uncertainty, not a full guarantee — but the gap is self-correcting. Because "neither file exists" is what triggers first-run in the first place, a persistence failure that slips through once surfaces again, unprompted: the next time the user opens this folder, it looks like a fresh first run with no tasks, which is itself the signal something didn't stick. Let that happen rather than manufacturing a check to preempt it.

### Status line

For a normal run (both files already exist), every entry point opens with exactly one line stating where things stand: what this folder is set up for (`config.yaml`'s `fund_name` if set, otherwise the folder name — never mention whether `fund_name` was set or not, just fall back silently), the open task counts from `todos.md`, and when `actions.md` last changed. Any deviation from what the user expects should be obvious from this one line alone. Keep it to one line — this is meant to be the recognizable opening of this tool, not a status dump. A first run or a partial-state flag replaces this line for that run — see "First run in a folder" above.

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
