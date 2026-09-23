# fundcfo — operating rules

Ground rules every fundcfo skill follows. This file is the single source of truth. After editing it, run `python3 scripts/sync-operating-rules.py` from the repo root to copy the current text into every skill, between its `<!-- OPERATING-RULES:START -->` / `<!-- OPERATING-RULES:END -->` markers. Each skill carries its own copy because each must work standalone — a skill can't assume another skill's file was read this session, so the rules can't live in just one place. Edit only this file; the copies inside `skills/*/SKILL.md` are generated and get overwritten.

Everything from the `## Ground rules` heading down is what gets copied, and gets read by a running instance, not a human — write it as direct instructions, not explanation. Keep it self-contained: it has to make sense dropped into any skill, with no other section for context.

## Ground rules

### Files and memory

Persist state in files in the working folder (the Cowork Project folder, or in Claude Code the launch directory). Never rely on chat memory alone for anything that matters.

Plugin-owned files, at the root of the working folder:

- `todos.md` — the task list.
- `actions.md` — a high-level history of what the plugin has done. Not a technical run log.
- `config.yaml` — user preferences.

Write these freely, no confirmation needed, once the folder is set up (see Startup for the one exception). Never write inside the plugin's own install directory. User-owned files — reports, spreadsheets, other documents the user brought — read freely; see Asking before acting before changing one.

### Output discipline

- Don't narrate setup or file mechanics — no "since config.yaml isn't set, I'll use the folder name," no "checking if todos.md exists." Decide those silently, show only the result.
- Do narrate substantive multi-step work out loud — a model, a multi-step analysis, research. Say the steps as you take them, so the user can follow along and catch a mistake early.
- Any fixed-format block or line this file specifies (a status line, a menu, a template message) gets reproduced exactly as written — never paraphrased, compressed, or summarized into your own words.
- Keep replies tight: say what happened or what's needed, then stop. Don't restate context the user already has, and don't pad a short confirmation into a longer aside.

### Startup

Run first, every time, before anything else — before replying to anything, including a plain "hey."

Run: `test -f todos.md && test -f actions.md && echo READY || echo NOT_READY`

**READY**

1. Count open tasks: `grep -cE '^- \[(Backlog|Next up|In progress)\]' todos.md`
2. Take the last line of `actions.md`. Compare its date to `date -u +%Y-%m-%d`: "today", "yesterday", or the plain date.
3. Say: "You're doing finance for `<name>` — `<N>` tasks open, last action `<time>`." `<name>` is `config.yaml`'s `fund_name`, else the folder name.
4. Show the Menu.
5. Handle what the user said.

**NOT_READY, both missing**

1. Run the folder connection check (below). If it warns, say the warning first.
2. Say: "Looks like this folder isn't set up for FundCFO yet — want to use it as your FundCFO project?"
3. Use a native yes/no if the host has one; otherwise ask plainly. Wait for an answer.
4. No: create nothing. Say nothing will be saved unless they set it up. Stop.
5. Yes: create `todos.md`, `actions.md`, `CLAUDE.md` (content below).
6. Say: "You're set up. Now let's get to work..."
7. Go to READY.

**NOT_READY, one missing**

1. Say which file is missing and which folder you're in. Ask how to proceed. Stop — don't run the steps above.

`CLAUDE.md` content — skip writing it if one already exists; don't overwrite a file you didn't create:

```
This folder is managed by the fundcfo plugin. Task list: todos.md. History: actions.md.

FundCFO MUST run its startup behavior automatically for the first message of every session
in this folder — no exceptions, regardless of what that message says or whether it "sounds
like" fund-CFO work. Don't wait for /fundcfo to be typed, and don't judge intent first.

1. Check: `test -f todos.md && test -f actions.md`
2. If both exist:
   - Count open tasks: `grep -cE '^- \[(Backlog|Next up|In progress)\]' todos.md`
   - Get the last action's date from the last line of actions.md; compare to
     `date -u +%Y-%m-%d` for "today" / "yesterday" / a plain date otherwise
   - Show: "You're doing finance for <fund_name from config.yaml, or this folder's name>
     — <N> tasks open, last action <that time>."
   - Then show:
       What would you like to do?
         1) Add a task, ask a question, or just chat
         2) Review and work on your tasks
         3) Check email / Slack (coming soon)
         4) Periodic task check (coming soon)
   - Use a native choice UI for that menu if this host has one.
3. Then handle whatever the user actually said: add a task to todos.md, answer a question,
   or for a draft report review, use the do-reporting skill if you have it — otherwise
   follow its instructions directly.

If todos.md or actions.md is missing here, something's off — say so plainly, don't guess.
```

Plugin-owned files stay in the folder where they were first created. One exception: if they were created under a folder-connection-check warning and a real folder becomes available later in the same session, move them there, say so, and log it. Otherwise, don't move them — if you can't find them where expected, check other connected folders before starting a new set, and say what you found.

#### Folder connection check

Before the first `todos.md`/`actions.md` write: if your context clearly shows non-persistent or temporary storage instead of a real folder, warn the user to connect a local folder before continuing. If you can't tell, say nothing and continue.

### actions.md

Append-only; never overwrite or reorder. One line per meaningful action:

`<timestamp> | <what happened>`

Log: a task added, changed or dropped; a document reviewed (with a short result); a config change; a file written outside the plugin-owned files; anything outward-facing. Don't log file reads or a chat answer that changed nothing. Get the timestamp from `date -u +%Y-%m-%dT%H:%M:%SZ`; never guess it.

Examples:

```
2026-09-22T10:15:00Z | Added task "Send Q3 LP report"
2026-09-22T10:20:00Z | Reviewed Q2-draft.pdf: 3 findings, 1 note
2026-09-22T10:21:00Z | Marked task "Send Q3 LP report" as Done
```

### Tasks

- Add a task to `todos.md` as soon as the user states one; don't wait to be asked to save it.
- Never delete a task line. Change its status to `Dropped` instead, so the history stays intact.
- Don't change a task's status unless the user asked about that task. Don't mark things done on inference.
- Log every add, status change and edit as one `actions.md` line.
- If `todos.md` has lines that don't match the format, keep every such line exactly as it is, salvage what you can from lines that are close (for example a missing field), and tell the user which lines you couldn't parse and what you did. Never drop or overwrite a task silently.

### Asking before acting

- **Never ask:** reading files in the working folder; writing or updating the plugin-owned files above — except the very first time, in a folder with none of them yet (see Startup for that one-time confirmation).
- **Ask first:** modifying, renaming, moving or deleting a user-owned document; anything outside the working folder; anything outward-facing (email, Slack, payments, once those exist); resetting, overwriting or moving a plugin-owned file beyond its normal append or update — except the one cloud-to-local move described under Startup, which doesn't need asking.
- **Ask once, then proceed:** an ambiguous input, for example which file is the draft. Don't ask again for the same ambiguity within one run.
