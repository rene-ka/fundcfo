# Changelog

## 0.5.0

Data gets a fixed home.

- Instructions are no longer written for a plugin only. They rely on no host features, so the same files can run in Cowork, Claude Code, an Agent SDK agent, a managed agent or another model. Data is found the same way everywhere, and shell commands say what they are for.
- Data lives in one root, `~/Documents/FundCFO` (or `FUNDCFO_HOME`), with one folder per project. The session's folder no longer matters, so the in/outside-a-working-folder logic, `AGENTS.md`/`CLAUDE.md` in the data, and auto-start on "hey" are gone.
- Projects: sticky active project; "switch project", "new project" and "move project". A project can live in any folder; the root config records where.
- `<home>/config.yaml` records the data version. Data upgrades list their changes and ask first. Folders from 0.4 or earlier are offered a move into the data root, or can stay where they are as a project.
- Startup asks for access to the data folder right away, for no more than it needs, and won't set up in an existing `Documents/FundCFO` folder that isn't FundCFO's.
- Update notice: once a day, FundCFO checks GitHub for a newer version and says how to update.
- Menu: dropped "Check email / Slack".

## 0.4.0

Structure for a complete plugin; little new content.

- Entry depends on location. In a working folder: status line and Menu, or straight to a request. Outside one: the plugin asks whether that's intentional and offers a question-only session, directions to the working folder, or setup. The Menu is now part of the shared rules.
- New working-folder layout: `tasks.md` (was `todos.md`), `log.md` (was `actions.md`), `handbook/` with processes and reference notes, `AGENTS.md` as the startup source with `CLAUDE.md` pointing to it. Existing folders are offered a rename.
- Process templates at the plugin root. The draft-report review moved there.
- Modes: `assistant` (default) and `auto`.
- Shared rules gain a General CFO approach. Startup checks the folder on every run and offers fixes instead of stopping.
- `config.yaml`: `team_name` replaces `fund_name`; new `mode` and `handbook` keys.
- First run seeds two tasks: Onboarding and Complete the handbook.

## 0.3.3

Narrower no-narration rule: setup and file mechanics only.

## 0.3.2

Design-rationale prose removed from the operational files.

## 0.3.1

Startup rebuilt inline; the entry skill can be invoked by the model.

## 0.3

Fixes from the second Cowork test round.

## 0.2.2

One cloud-to-local move allowed for plugin-owned files.

## 0.2.1

Dropped the step asking the user to check Finder.

## 0.2

Fixes from the first smoke test in Claude Code.

## 0.1

First version: the Do reporting skill, with draft-report review.
