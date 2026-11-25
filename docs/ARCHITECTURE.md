# Architecture

fundcfo is a static plugin. It holds no state of its own. On first run it sets up one working folder for the team's whole setup, across all funds and vehicles. From then on, everything the plugin learns and does lives in that folder.

## Entry points

The plugin first checks whether it's running in a working folder (a folder set up for fundcfo).

- **In a working folder**: `/fundcfo` or a plain "hey" shows a one-line status and the Menu. A skill called with a request goes straight to it.
- **Outside a working folder**: `/fundcfo` asks whether that's intentional, with three answers: just a question (nothing is saved), how to get to the working folder, or set up a working folder here. A skill called with a request does the work and notes that nothing is saved.

Any other skill called without a request asks what the user wants to do with it.

The Menu is fixed and part of the shared operating rules:

1. Add a task, ask a question, or just chat
2. Review and work on your tasks
3. Check email / Slack (coming soon)
4. Periodic task check (coming soon)

## How it fits together

**Shipped with the plugin**

- **CFO skills**: the ways a CFO works, such as reviewing tasks, exploring the structure, reporting, risk, modelling and interpreting contracts. They carry judgment and know-how, not fixed procedures. Background material that isn't judgment or procedure sits in a skill's `references/` folder.
- **General CFO approach**: the judgment every skill applies. It is part of the shared operating rules, not a skill of its own.
- **Plugin skills**: what the plugin itself does. These are startup and housekeeping on every run, and turning a process template into a process.
- **Process templates**: generic how-tos for recurring work, such as quarterly reporting, including common pitfalls and important notes. CFO skills link to them where a procedure matters.

**Built up in the working folder**

- **Handbook**: the high-level description of the setup, plus:
  - **Processes**: process templates copied into the handbook and adapted. For example: "Quarterly reporting: the admin sends data on day 10, the Excel file lives here, Sam reviews." A process can point to other processes as sub-processes. A process is amended whenever a task shows that something isn't spelled out.
  - **Reference notes**: file locations, structure chart, people, service providers, tech setup.
- **Tasks**: the core of day-to-day work. A task is a single piece of work, such as "Q1 2027 reporting". It is a short stub that links to its process and holds only what's specific to that piece of work. Tasks run on a kanban board:
  - **Backlog**: known, not yet scheduled.
  - **Next up**: to start soon.
  - **In progress**: being worked on.
  - **Done**: finished. Never rewritten.
  - **Dropped**: not pursued. Kept for the record, never deleted.
- **Log**: what the plugin has done, one line per action.
- **Config**: preferences, mode, and the paths to anything kept outside the folder.

## Plugin layout

```
.claude-plugin/plugin.json
OPERATING-RULES.md        shared rules incl. General CFO approach; copied into every skill
process-templates/        shipped process templates
skills/
  fundcfo/                entry point and plugin skills
  <cfo-skill>/            SKILL.md + references/
scripts/                  dev tooling (sync-operating-rules.py)
docs/                     this file, roadmap, changelog
```

Skills refer to process templates by relative path (`../../process-templates/` from a `SKILL.md`), and the operating rules describe this layout, so any host that can read the plugin folder can follow the links.

`OPERATING-RULES.md` is the single source of the rules every skill follows. Each `SKILL.md` carries a copy between `<!-- OPERATING-RULES:START -->` and `<!-- OPERATING-RULES:END -->`, because a skill can't assume another skill's file was read in the session. After editing it:

```
python3 scripts/sync-operating-rules.py
claude plugin validate .
```

To package, name the zip after `plugin.json`'s version:

```
VERSION=$(python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])")
zip -r fundcfo-$VERSION.zip .claude-plugin skills process-templates
```

## Working folder layout

```
AGENTS.md                 startup instructions for any agent; source of truth
CLAUDE.md                 points to AGENTS.md
config.yaml
tasks.md
log.md
handbook/
  README.md               overview, process calendar, open gaps
  processes/
  reference/
```

Any part of the handbook can live outside the working folder (for example, on a shared drive). `config.yaml` then holds its path, and the plugin reads and writes it there.

## Modes

Set in `config.yaml`:

- **assistant** (default): proposes what it is about to do and waits for a yes.
- **auto**: does it, then says what it did.

## Hosts and models

The plugin is built for Claude (Cowork, Claude Code) but is not tied to it. It doesn't depend on host features such as project memory. Startup instructions live in a plain `AGENTS.md`, and all paths are relative, so the same plugin can inform an agent built with the Agent SDK, a managed agent, or another model.
