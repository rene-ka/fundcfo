# fundcfo

fundcfo.ai: an assistant for the CFO of a VC fund. It runs in Claude Cowork and Claude Code, and its instructions can inform other agents too.

## How it works (TL;DR)

- **CFO skills** bring the judgment: how a CFO thinks about tasks, reporting, risk, modelling or contracts.
- FundCFO ships **process templates**: generic how-tos for fund-CFO work, such as quarterly reporting, with common pitfalls and important notes.
- Your data lives in one place, `~/Documents/FundCFO`, with one **project** per setup (most people have one). A project holds your **handbook** for the whole setup, across all funds and vehicles. Its **processes** are the templates copied and adapted to your setup: who does what, where the files are, which deadlines apply.
- Day-to-day work runs as **tasks** ("Q1 2027 reporting"): short entries that point to a process and move across a kanban board (Backlog, Next up, In progress, Done, Dropped). When a task shows that the process is missing something, the process gets updated for next time.
- `/fundcfo` gives you a status line and a fixed Menu. You can also call any skill directly.
- By default FundCFO proposes what it's about to do and waits for your yes. In auto mode it just does it and tells you what it did.

More detail: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## CFO skills

Explore and learn about the structure · Review overall tasks (CFO 360) · Do a specific task · Drive a process · Confirm or check something · Do reporting · Answer fund dynamics and LPA questions · Look at something from a risk perspective · Strategize on operations · Strategize on the fund · Model something · Research something · Prepare payments · Create or review financial accounts · Exegesis: interpret rules, regulation and contracts

## Status

**Version 0.5.0 (pilot).** The structure is in place: data root and projects, handbook, tasks, process templates and the CFO skills list. Most CFO skills are not live yet. See [docs/ROADMAP.md](docs/ROADMAP.md).

Live now:

- **Tasks**: add, review and work through your task list.
- **Do reporting → Review a draft report.** It cross-checks a draft report and flags disagreements for you to judge. You give it the draft, plus whatever you have of:
  - the final report of the past quarter, or the last two
  - your internal Excel file with the reporting data
  - Word files or other documents with the qualitative parts
  - any other source the report shouldn't contradict, such as portfolio-company reporting

  It goes through every number and paragraph, looking for figures that differ between places or sources, names that change, and figures that don't fit together. You get a list of observations, for example "IRR 5.4% on pg. 3 vs 5.2% on pg. 2", split into exact findings and general notes. It doesn't decide which figure is right, and it doesn't reconcile against a ledger.

## Setup

### Claude Cowork

Built for Cowork (Claude desktop app, paid plan).

1. Download `fundcfo-<version>.zip` from [GitHub releases](https://github.com/rene-ka/fundcfo/releases).
2. In Cowork, add it as a custom plugin by uploading the zip.
3. Type `/fundcfo` in any chat or Project. On first use it asks for access to `~/Documents/FundCFO`, asks what to call your first project, and sets it up. To grant as little as possible, create an empty `FundCFO` folder in Documents first.

### Claude Code

```
git clone https://github.com/rene-ka/fundcfo.git
claude --plugin-dir ./fundcfo
```

Clone it anywhere except straight into Documents: a `fundcfo` folder there would clash with FundCFO's data folder, `~/Documents/FundCFO`. Then type `/fundcfo`. First use works as in Cowork.

### Anywhere else

No recipe yet, but FundCFO is plain Markdown and isn't tied to Claude. Point your agent (Agent SDK, a managed agent, another model) at `skills/fundcfo/SKILL.md`, give it file access, and set `FUNDCFO_HOME` to a folder that persists. If you get it running, open an issue and tell us how. We'd love to add your setup here.

### Your data, updates and older versions

Your data stays in `~/Documents/FundCFO` whichever folder a session runs in.

To update, download the latest release from [GitHub releases](https://github.com/rene-ka/fundcfo/releases) and add it the same way, replacing the old one. FundCFO tells you when a new version is out.

If you used FundCFO 0.4 or earlier, open a session in your old folder and type `/fundcfo`. It offers to move that data into `~/Documents/FundCFO` as a project, or to keep it where it is.

## Using it

`/fundcfo` opens with a one-line status ("You're doing finance for Acme Ventures — 2 tasks open, last action today"), then the Menu:

```
What would you like to do?
  1) Add a task, ask a question, or just chat
     Try: "review my quarterly report"
  2) Review and work on your tasks
  3) Periodic task check (coming soon)
```

You can also call any skill directly, such as `/do-reporting` with a draft. Say "switch project" or "new project" to work with more than one setup, and "move project" to keep a project in another folder, such as a shared drive.

## Data handling

- Sent to Anthropic when you run it: the documents you work on and your tasks and handbook, which may contain deal or people names.
- Stored only on your machine, in `~/Documents/FundCFO`, or wherever you keep a project or handbook.
- FundCFO asks the Claude app for access to `Documents/FundCFO` only. If that folder doesn't exist yet, it offers to create it.
- Once a day, FundCFO reads its latest version number from this GitHub repo and tells you if an update is available. Nothing about you or your data is sent.
- Nothing reaches fundcfo.ai's servers. There are none.

## Credits

Inspired by [gstack](https://github.com/garrytan/gstack).
