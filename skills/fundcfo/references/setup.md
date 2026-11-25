# Setup

Run when the user chooses to set up a working folder here.

1. **Folder check.** If your context clearly shows non-persistent or temporary storage instead of a real folder, warn the user to connect a local folder first. If you can't tell, say nothing.
2. **Create** the files below. If a file already exists, leave it as it is.
   - `CLAUDE.md` already exists and isn't yours: offer to append the line `See AGENTS.md for FundCFO.` instead.
   - Get the timestamp from `date -u +%Y-%m-%dT%H:%M:%SZ`.
3. Say: "You're set up. Now let's get to work..."

If files were created under a folder-check warning and a real folder becomes available later in the same session, move them there, say so, and log it. Otherwise never move them. If you can't find them where expected, check other connected folders before starting a new set, and say what you found.

## Files

`AGENTS.md`:

```
# FundCFO

This folder is managed by the fundcfo plugin. Tasks: tasks.md. History: log.md.
Handbook: handbook/, or the path set as `handbook:` in config.yaml.

Run FundCFO's startup for the first message of every session in this folder, whatever
the message says. Don't wait for /fundcfo to be typed, and don't judge intent first.

If the fundcfo plugin is available, use its fundcfo skill. Otherwise:

1. Count open tasks: `grep -cE '^- \[(Backlog|Next up|In progress)\]' tasks.md`.
   Compare the date of log.md's last line to `date -u +%Y-%m-%d`: "today", "yesterday",
   or the plain date.
2. Say: "You're doing finance for <team_name from config.yaml, or this folder's name>
   — <N> tasks open, last action <that time>."
3. Show, with a native choice UI if the host has one:
     What would you like to do?
       1) Add a task, ask a question, or just chat
       2) Review and work on your tasks
       3) Check email / Slack (coming soon)
       4) Periodic task check (coming soon)
4. Handle what the user said. Tasks are one line each in tasks.md:
   `- [status] name | description | due date | people`, status one of Backlog,
   Next up, In progress, Done, Dropped. Never delete a task; set it to Dropped.
   Log every change to log.md as `<date -u +%Y-%m-%dT%H:%M:%SZ> | <what happened>`.
5. When a piece of work is done, say what's next on that task and show the menu again.

If tasks.md or log.md is missing, say so plainly; don't guess.
```

`CLAUDE.md`:

```
@AGENTS.md

See AGENTS.md for FundCFO.
```

`config.yaml`:

```
mode: assistant
```

`tasks.md`:

```
- [Next up] Onboarding | Get a sense of the setup: what exists, where it lives, who does what. Anything without a process goes to Open gaps in the handbook. | |
- [Backlog] Complete the handbook | Write up the setup's processes, working through Open gaps | |
```

`log.md`:

```
<timestamp> | Set up FundCFO in this folder
```

`handbook/README.md`:

```
# Handbook

## Overview

How the setup is structured: funds, vehicles, team. Filled in during onboarding.

## Tasks

Work is tracked in tasks.md, one line per task, on a kanban board:

- **Backlog**: known, not yet scheduled.
- **Next up**: to start soon.
- **In progress**: being worked on.
- **Done**: finished. Never rewritten.
- **Dropped**: not pursued. Kept for the record.

A task stays short and points to its process in processes/ for the how-to.

## Process calendar

Recurring processes and when they run.

## Processes

One file per process in processes/.

## Open gaps

Things the setup has no process for yet.
```

Create `handbook/processes/` and `handbook/reference/` when the first file goes into them.
