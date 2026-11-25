# Changelog

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
