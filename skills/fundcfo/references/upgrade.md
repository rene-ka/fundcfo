# Upgrade

## Old working folder

The current folder holds FundCFO data from version 0.4 or earlier, when the data lived in whatever folder the session ran in.

1. Ask, with a native choice if the host has one. `<slug>` is the folder's name, made as in `setup.md`:

   ```
   This folder holds FundCFO data from an earlier version. FundCFO now keeps its data in <home>, with a separate project folder for each setup.
     1) Move it into its own project folder, <home>/<slug>
     2) Keep it here as its own project, "<slug>"
     3) Not now
   ```

2. **Move or keep:**
   - `<home>/config.yaml` missing: create it as `setup.md`, First run, step 3 describes.
   - Move: create `<home>/<slug>/` and move into it `tasks.md`, `todos.md`, `log.md`, `actions.md`, `config.yaml` and `handbook/`, whichever exist. Keep: leave them where they are, and add `<slug>: <path of this folder>` under `projects` in `<home>/config.yaml`.
   - Rename `todos.md` to `tasks.md` and `actions.md` to `log.md`.
   - In the project's `config.yaml`: rename `fund_name` to `team_name`, and add `mode: assistant` if `mode` is missing. No `config.yaml`: create it as `setup.md`, Project files, describes.
   - Create any other Project file that's missing.
   - Set `active_project` in `<home>/config.yaml` to `<slug>`, and log `<timestamp> | Moved working folder <path> into FundCFO as project <slug>` or `<timestamp> | Added working folder <path> as project <slug>`.
   - `CLAUDE.md` or `AGENTS.md` written by FundCFO (starting with "This folder is managed by the fundcfo plugin" or "# FundCFO"): offer to delete them. They're no longer used.
   - Say: "Done. Your data is now in `<project folder>`."
3. **Not now:** change nothing. Ask again next session.

Then continue with Startup step 3.

## Data upgrades

Run when `<home>/config.yaml` has no `version`, or an older one than FundCFO's.

1. Collect the steps below for every version newer than the data's. If there are none, set `version` to FundCFO's version and carry on without saying anything.
2. Otherwise ask, with a native yes/no if the host has one. List only the steps that apply:

   ```
   Your FundCFO data was last used with <version, or "an earlier version">.
   Version <FundCFO version> needs these changes:
     - <one line per step>
   Upgrade now?
   ```

3. **Yes:** apply the steps, set `version`, and log `<timestamp> | Upgraded data to FundCFO <version>` in every project changed. Say "Upgrade done." in one line.
4. **No:** say "FundCFO may not work properly until the data is upgraded. I'll ask again next session." Carry on without changing anything.

Then continue with Startup step 6.

### Steps to 0.5.0

None.
