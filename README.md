# fundcfo

fundcfo.ai: an assistant for the CFO of a VC fund, packaged as a Claude plugin.

## How it works (TL;DR)

- **CFO skills** bring the judgment: how a CFO thinks about tasks, reporting, risk, modelling or contracts.
- The plugin ships **process templates**: generic how-tos for fund-CFO work, such as quarterly reporting, with common pitfalls and important notes.
- One working folder holds your **handbook** for the whole setup, across all funds and vehicles. Its **processes** are the templates copied and adapted to your setup: who does what, where the files are, which deadlines apply.
- Day-to-day work runs as **tasks** ("Q1 2027 reporting"): short entries that point to a process and move across a kanban board (Backlog, Next up, In progress, Done, Dropped). When a task shows that the process is missing something, the process gets updated for next time.
- Open a session in your working folder and you get a status line and a fixed Menu. You can also call any skill directly, even outside a working folder, for one-off work that isn't saved.
- By default the plugin proposes what it's about to do and waits for your yes. In auto mode it just does it and tells you what it did.

More detail: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## CFO skills

Explore and learn about the structure · Review overall tasks (CFO 360) · Do a specific task · Drive a process · Confirm or check something · Do reporting · Answer fund dynamics and LPA questions · Look at something from a risk perspective · Strategize on operations · Strategize on the fund · Model something · Research something · Prepare payments · Create or review financial accounts · Exegesis: interpret rules, regulation and contracts

## Status

**Version 0.4.0 (pilot).** The structure is in place: working folder, handbook, tasks, process templates and the CFO skills list. Most CFO skills are not live yet. See [docs/ROADMAP.md](docs/ROADMAP.md).

Live now:

- **Tasks**: add, review and work through your task list.
- **Do reporting → Review a draft report.** It cross-checks a draft report and flags disagreements for you to judge. You give it the draft, plus whatever you have of:
  - the final report of the past quarter, or the last two
  - your internal Excel file with the reporting data
  - Word files or other documents with the qualitative parts
  - any other source the report shouldn't contradict, such as portfolio-company reporting

  It goes through every number and paragraph, looking for figures that differ between places or sources, names that change, and figures that don't fit together. You get a list of observations, for example "IRR 5.4% on pg. 3 vs 5.2% on pg. 2", split into exact findings and general notes. It doesn't decide which figure is right, and it doesn't reconcile against a ledger.

## Setup

Built for Claude Cowork (desktop app, paid plan). It also runs in Claude Code.

1. Install the plugin: in Cowork, add it as a custom plugin file (a zip of this repo's plugin folders).
2. Create a Cowork Project with **Use an existing folder**, pointing at a dedicated folder.
3. In that Project, type `/fundcfo`. The first run sets up the folder.

Connect a real folder. Without one, files may not be there in your next chat. If you see the first-run message again on a folder you've been using, that's the sign: connect the folder and it picks up from there.

## Using it

`/fundcfo` opens with a one-line status ("You're doing finance for Acme Ventures — 2 tasks open, last action today"), then the Menu:

```
What would you like to do?
  1) Add a task, ask a question, or just chat
     Try: "review my quarterly report"
  2) Review and work on your tasks
  3) Check email / Slack (coming soon)
  4) Periodic task check (coming soon)
```

Once a working folder is set up, you don't need to type `/fundcfo` again there: a plain "hey" starts it. You can also call any skill directly at any time. Outside a working folder, the plugin still answers questions and does one-off work, but saves nothing.

## Data handling

- Sent to Anthropic when you run it: the documents you work on and your tasks and handbook, which may contain deal or people names.
- Stored only in your working folder (and wherever you point the handbook).
- Nothing reaches fundcfo.ai's servers. There are none.

## Credits

Inspired by [gstack](https://github.com/garrytan/gstack).
