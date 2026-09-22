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

Write these freely, without asking for confirmation, once the folder is set up (see "First run in a folder" for the one exception). Never write inside the plugin's own install directory, which is replaced on every update. User-owned files (the reports, spreadsheets and other documents the user brought) are different: read them freely, but see "Asking before acting" below before changing one.

### Output discipline

- Never narrate your own reasoning or decisions to the user — no "since X isn't set, I'll use Y," no thinking out loud. Decide silently; show only the result.
- Any fixed-format block or line this file specifies (the Status line, the Menu, a first-run message) gets reproduced exactly as written — never paraphrased, compressed, or summarized into your own words.
- Keep replies tight: say what happened or what's needed, then stop. Don't restate context the user already has, and don't pad a short confirmation into a longer aside.

### First run in a folder

The setup set is three files, always created together: `todos.md`, `actions.md`, and a pointer file, `CLAUDE.md` (content below). `config.yaml` is separate — created later, only when the user states a preference.

Before doing anything else, check whether `todos.md` and `actions.md` exist:

- **Both exist:** normal — see Status line.
- **Only one exists:** flag it in one line — name the missing file and the folder you're in — before continuing. It means a file was moved or deleted, or the user is in a different folder than usual. Don't run the confirmation below for this case; just recreate the missing one.
- **Neither exists:** genuine first run. Run the folder connection check below first — if it finds a clear signal, lead with that warning. Then ask, once, before creating anything: "Looks like this folder isn't set up for FundCFO yet — want me to set it up here? I'll create `todos.md`, `actions.md` and a small `CLAUDE.md` pointer." Wait for a clear yes. This is the one time creating these files needs asking — every other plugin-owned write doesn't, and don't ask again once a folder is set up. It's what stops the skill writing into whatever folder happens to be open if it gets invoked somewhere by mistake. If the user declines, create nothing; answer normally for this exchange, and say plainly that nothing will be saved here unless they set it up.

Once confirmed, create all three files immediately, in the same reply — don't wait for the user's first task or first loggable action to trigger it. (That used to be the rule; it was unreliable, since a first message that's just a question never counted as either, so the files sometimes never got created at all even in an empty folder.) After creating them, continue straight into the Menu, same reply, no separate confirmation paragraph in between — see Output discipline above.

`CLAUDE.md`'s content — skip writing it if one already exists in the folder; don't overwrite a file you didn't create, but still create `todos.md`/`actions.md` as normal:

```
This folder is managed by the fundcfo plugin. Task list: todos.md. History: actions.md.
If the user asks about their tasks, a report review, or other fund-CFO work in this folder,
go ahead and follow the fundcfo skill yourself, exactly as if `/fundcfo` had been typed —
you don't need them to type it.
```

This eager behavior only applies inside a folder carrying this file. Outside one, `disable-model-invocation: true` on the fundcfo skill still means it never starts on its own.

Plugin-owned files always stay in the folder they were first created in, with exactly one exception: if they were first created under a folder-connection-check warning (flagged as non-persistent, temporary or account-level storage) and, later in that same session, a real local folder becomes available, move `todos.md`, `actions.md` and `config.yaml` there — write the content into the new location, then stop writing to the old one. This is the only case a move is ever allowed, and it only makes sense within the same session: once the chat ends, whatever was left in non-persistent storage is gone regardless, so there's nothing left to rescue afterward. Do the move without asking, same as any other plugin-owned write, but say plainly what happened — name both the flagged location and the new folder — and log it as one `actions.md` line in the new location.

Outside that one case, granting access to more folders later (for reading comparison sources, say) never changes where these files live. If you expect them and don't find them in the current folder, check other connected folders before treating it as a fresh first run — say what you found, and use that location, rather than silently starting a second set elsewhere.

#### Folder connection check

Persistence depends on a real, connected folder, and there's no confirmed way to know from inside a skill whether one exists — it may vary by host. Before writing `todos.md`/`actions.md` for the first time, look at whatever your own context tells you about where that write will land. Only act on a clear signal: if what you can see plainly indicates non-persistent, temporary or account-level storage rather than a real folder on the user's machine, say so and tell them to connect a local folder before relying on anything from this session. If you can't tell either way — no clear signal, or a path that looks like an ordinary folder — say nothing about it and proceed as an ordinary first run. Don't ask the user to go check anything themselves; a warning on a guess is worse than no warning.

This is deliberately quiet on uncertainty, not a full guarantee — but the gap is self-correcting. Because "neither file exists" is what triggers first-run in the first place, a persistence failure that slips through once surfaces again, unprompted: the next time the user opens this folder, it looks like a fresh first run with no tasks, which is itself the signal something didn't stick. Let that happen rather than manufacturing a check to preempt it.

### Status line

For a normal run (both files already exist), every entry point opens with exactly one line, this shape: "You're doing finance for `<name>` — `<N>` task`<s>` open, last action `<friendly time>`." `<name>` is `config.yaml`'s `fund_name` if set, otherwise the folder name — fall back silently, don't narrate the decision (see Output discipline). `<N>` is the count of tasks not `Done` or `Dropped` — don't break it down by status here, that's what Menu option 2 is for. `<friendly time>` is human, never a raw timestamp: "today," "yesterday," or a plain date. Example: "You're doing finance for StellarFund — 2 tasks open, last action today." Any deviation from what the user expects should be obvious from this one line alone. Keep it to exactly this one line — this is meant to be the recognizable opening of this tool, not a status dump. A first-run confirmation or a partial-state flag replaces this line for that run — see "First run in a folder" above.

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

- **Never ask:** reading files in the working folder; writing or updating the plugin-owned files above — except the very first time, in a folder with none of them yet (see "First run in a folder" for that one-time confirmation).
- **Ask first:** modifying, renaming, moving or deleting a user-owned document; anything outside the working folder; anything outward-facing (email, Slack, payments, once those exist); resetting, overwriting or moving a plugin-owned file beyond its normal append or update — except the one cloud-to-local move described under "First run in a folder," which doesn't need asking.
- **Ask once, then proceed:** an ambiguous input, for example which file is the draft. Don't ask again for the same ambiguity within one run.

### References and highlights

A skill can hold a `references/` folder, one file per task it supports (for example `do-reporting/references/review.md`). The skill's own `SKILL.md` stays short: it names its tasks and says which are live. A reference file can mark itself `highlight: true` in its front matter with a one-line `try:` prompt; the `/fundcfo` entry point's Menu surfaces every highlighted, live reference this way, under option 1. A reference with no `highlight` is still usable, just not surfaced.
