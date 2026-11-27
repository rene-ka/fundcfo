# Setup

## First run

Run when `<home>/config.yaml` doesn't exist.

1. If the environment looks non-persistent (for example, a sandbox with no mounted storage), warn that the data may not survive this session.
2. Say: "FundCFO keeps its data in `<home>`, with a separate project folder for each setup. Most people need just one. What should I call your first project? Usually your firm's name." Wait for the answer.
3. Create `<home>/config.yaml`. Take `version` from `../../.claude-plugin/plugin.json` (relative to this skill's folder). `<slug>` is the name in lowercase with hyphens for spaces, for example `acme-ventures`.

   ```
   active_project: <slug>
   version: <version>
   ```

4. Create the Project files below in `<home>/<slug>/`.
5. Say: "You're set up. Now let's get to work..." Then say the status line and show the Menu.

## Project files

Used by First run and by "New project". Get the timestamp from the clock (`date -u +%Y-%m-%dT%H:%M:%SZ`). If a file already exists, leave it as it is.

`config.yaml`:

```
team_name: <name>
mode: assistant
```

`tasks.md`:

```
- [Next up] Onboarding | Get a sense of the setup: what exists, where it lives, who does what. Anything without a process goes to Open gaps in the handbook. | |
- [Backlog] Complete the handbook | Write up the setup's processes, working through Open gaps | |
```

`log.md`:

```
<timestamp> | Created project <name>
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
