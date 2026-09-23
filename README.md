# fundcfo

fundcfo.ai — an assistant for the CFO of a VC fund, packaged as a Claude Cowork plugin.

**Version 0.3.2 (pilot)** — one working mode: **Do reporting**, with a **Review** task for draft quarterly reports.

## What it does

The plugin is built around the different ways a fund CFO works: reporting, checking, modelling, answering LPA questions and so on — see `OPERATING-RULES.md` and `skills/fundcfo/SKILL.md` for the full list. Only reporting is live in this version, and only its Review task.

**Review** cross-checks a draft report and flags disagreements for you to judge. You give it the draft, plus whatever you have of:

- the final report of the past quarter, or the last two
- your internal Excel file with the reporting data
- Word files or other documents with the qualitative parts
- any other source the report shouldn't contradict, such as portfolio-company reporting

It goes through every number and paragraph and looks for figures that differ between places or sources, names that change, and figures that don't fit together. The reply is a list of observations, for example "IRR 5.4% on pg. 3 vs 5.2% on pg. 2", each with a one-sentence explainer, split into exact findings and general notes. The observations live in the chat reply, not in a file — only a one-line summary is logged.

It flags disagreements between documents. It doesn't decide which figure is right, and it doesn't reconcile against a ledger.

## Setup

Requires Claude Cowork (desktop app) on a paid plan.

1. Install the plugin: in Cowork, add it as a custom plugin file (a zip of this repo's plugin folders).
2. Create a Cowork Project with **Use an existing folder**, pointing at a dedicated folder for your fund reports. Put the draft report there, and any comparison sources you have.
3. In that Project, type `/fundcfo`.

Use a dedicated folder, and connect it. If you start a Project without connecting a real folder, files still get written somewhere, but they may not be there in your next chat. The first run warns about this when there's a clear sign it's happening — if you ever see the first-run message again on a folder you'd already been using, that's the tell: connect a real folder and it'll pick up from there.

The first time it's invoked in a new folder, it asks before setting anything up — "Looks like this folder isn't set up for FundCFO yet — want to use it as your FundCFO project?" — rather than writing into whatever folder happens to be open. Say yes and it creates the files below, confirms with "You're set up. Now let's get to work...", and goes straight into the normal opening.

## Usage

`/fundcfo` opens with a one-line status ("You're doing finance for Acme Fund — 2 tasks open, last action today"), then the Menu. Once a folder is set up, you don't need to type `/fundcfo` again in that folder — asking about your tasks, or anything fund-CFO related, runs it directly, including on a plain "hey."

```
What would you like to do?
  1) Add a task, ask a question, or just chat
     Try: "review my quarterly report"
  2) Review and work on your tasks
  3) Check email / Slack (coming soon)
  4) Periodic task check (coming soon)
```

Each run writes to your Project folder:
- `actions.md`: a high-level history of what the plugin has done — a task added, a report reviewed, and so on. One line per action, appended every run.
- `todos.md` and `config.yaml`: your task list and preferences.
- `CLAUDE.md`: written once, on the first run only (skipped if you already have one). It's a self-sufficient copy of the opening behavior — status line, menu, task/question handling — so a plain "hey" or "what tasks do we have?" in this folder runs it directly, with no dependency on the `fundcfo` skill itself being invoked.

Plugin-owned files stay wherever they were first created — connecting more folders later, to read other sources, never moves them.

## Data handling

- Sent to Anthropic when you run it: the draft report, the comparison sources, and your task list, which may contain deal or people names.
- Stored only on your machine, in your Cowork Project folder: `actions.md`, `todos.md`, `config.yaml`.
- Nothing reaches fundcfo.ai's servers. There are none.

## Repository layout

```
.claude-plugin/plugin.json
OPERATING-RULES.md                          shared ground rules: files, logging, tasks, asking permission
scripts/sync-operating-rules.py             copies OPERATING-RULES.md into every skill (run after editing it)
skills/fundcfo/                             the /fundcfo entry point: working modes, status line, Menu
skills/do-reporting/                        the reporting mode
skills/do-reporting/references/review.md    the Review task's instructions
```

To package for sharing, name the zip after `plugin.json`'s current version:

```
VERSION=$(python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])")
zip -r fundcfo-$VERSION.zip .claude-plugin skills
```

## Development

`OPERATING-RULES.md` is the single source of truth for the rules every skill follows (file roles, logging, task handling, when to ask permission). Each `skills/*/SKILL.md` carries its own copy, between `<!-- OPERATING-RULES:START -->` / `<!-- OPERATING-RULES:END -->` markers, because a skill can't assume another skill's file was read this session. After editing `OPERATING-RULES.md`, run:

```
python3 scripts/sync-operating-rules.py
```

then `claude plugin validate .` before committing.
