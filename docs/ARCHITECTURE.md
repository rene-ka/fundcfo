# Architecture

FundCFO is two things: **instructions** and **data**.

- **Instructions**: the skills, shared rules and process templates. They are static, versioned and read-only, and an update replaces them wholesale. In Cowork and Claude Code they are installed as a plugin, and the host decides where that copy lives.
- **Data**: everything FundCFO learns and does for you. It lives in one data root, `~/Documents/FundCFO`. Hosts that can set environment variables, such as a sandboxed agent, can point the `FUNDCFO_HOME` variable elsewhere. Updating the instructions never overwrites it.

## Starting up

Whichever skill is called, FundCFO first finds the data root:

- **No data root yet**: first-run setup. It asks for a name and creates the root and a first project.
- **Data from an older version**: it says what will change and asks before upgrading. A folder from 0.4 or earlier, which kept its data in the session folder, is offered a move into the data root as a project.
- **Otherwise**: it opens the active project. `/fundcfo` on its own shows a one-line status and the Menu, any other skill on its own asks what you want to do, and any skill called with a request goes straight to it.

The Menu is fixed and part of the shared operating rules:

1. Add a task, ask a question, or just chat
2. Review and work on your tasks
3. Periodic task check (coming soon)

## How it fits together

**Instructions**

- **CFO skills**: the ways a CFO works, such as reviewing tasks, exploring the structure, reporting, risk, modelling and interpreting contracts. They carry judgment and know-how, not fixed procedures. Background material that isn't judgment or procedure sits in a skill's `references/` folder.
- **General CFO approach**: the judgment every skill applies. It is part of the shared operating rules, not a skill of its own.
- **System skills**: what FundCFO itself does. These are startup on every run, setup, upgrades, and turning a process template into a process.
- **Process templates**: generic how-tos for recurring work, such as quarterly reporting, including common pitfalls and important notes. CFO skills link to them where a procedure matters.

**Data, per project**

A project is one team's setup across all its funds and vehicles. Most people have one. A second can be useful for experimenting, or for running CFO services for several managers. The active project stays active until you switch. A project lives in the data root by default, but can live in any folder, such as a shared drive or one that isn't synced to the cloud; the root config records where.

- **Handbook**: the high-level description of the setup, plus:
  - **Processes**: process templates copied into the handbook and adapted. For example: "Quarterly reporting: the admin sends data on day 10, the Excel file lives here, Sam reviews." A process can point to other processes as sub-processes. A process is amended whenever a task shows that something isn't spelled out.
  - **Reference notes**: file locations, structure chart, people, service providers, tech setup.
- **Tasks**: the core of day-to-day work. A task is a single piece of work, such as "Q1 2027 reporting". It is a short stub that links to its process and holds only what's specific to that piece of work. Tasks run on a kanban board:
  - **Backlog**: known, not yet scheduled.
  - **Next up**: to start soon.
  - **In progress**: being worked on.
  - **Done**: finished. Never rewritten.
  - **Dropped**: not pursued. Kept for the record, never deleted.
- **Log**: what FundCFO has done, one line per action.
- **Config**: team name, mode, and the handbook's path if it's kept elsewhere.

Your own documents, such as a draft report to review, stay wherever they are. FundCFO reads them from there.

## Data layout

```
~/Documents/FundCFO/           or $FUNDCFO_HOME
  config.yaml                  active project, project locations, data version
  acme-ventures/               one folder per project, here or elsewhere
    config.yaml                team name, mode, handbook path
    tasks.md
    log.md
    handbook/
      README.md                overview, task statuses, process calendar, open gaps
      processes/
      reference/
```

A project's handbook can live elsewhere, such as on a shared drive. Its `config.yaml` then holds the path.

All data is plain Markdown and YAML, so anything with file access can read and write it.

## Instructions layout

```
.claude-plugin/plugin.json
OPERATING-RULES.md        shared rules incl. General CFO approach; copied into every skill
process-templates/        shipped process templates
skills/
  fundcfo/                entry point and system skills (references/setup.md, upgrade.md)
  <cfo-skill>/            SKILL.md + references/
scripts/                  dev tooling (sync-operating-rules.py)
docs/                     this file, roadmap, changelog
```

Instruction files refer to each other by relative path (`../../process-templates/` from a `SKILL.md`), never through host-specific variables.

`OPERATING-RULES.md` is the single source of the rules every skill follows. Each `SKILL.md` carries a copy between `<!-- OPERATING-RULES:START -->` and `<!-- OPERATING-RULES:END -->`, because a skill can't assume another skill's file was read in the session. After editing it:

```
python3 scripts/sync-operating-rules.py
claude plugin validate .
```

To release: bump `version` in `plugin.json`, merge to `main` (the update check reads `plugin.json` there), and attach the zip to a GitHub release. Name the zip after the version:

```
VERSION=$(python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])")
zip -r fundcfo-$VERSION.zip .claude-plugin skills process-templates
```

## Modes

Set per project:

- **assistant** (default): proposes what it is about to do and waits for a yes.
- **auto**: does it, then says what it did.

## Hosts and models

FundCFO is built for Claude (Cowork, Claude Code) but not tied to it. It relies on no host features: one data root found the same way everywhere, relative paths between instruction files, plain-text data, a choice UI only where the host has one, and every shell command paired with what it is for. The same instructions can therefore inform an agent built with the Agent SDK, a managed agent, or another model. In a sandbox, mount persistent storage and point `FUNDCFO_HOME` at it.
