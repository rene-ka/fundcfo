---
name: review
description: Cross-check a draft quarterly or other fund report for inconsistencies against other sources and against itself.
live: true
highlight: true
try: "review my quarterly report"
---

# Review

The user gives you a draft report, which is normally a PDF but could be a docx or similar. You check its data for internal consistency and against other data. This is a checkmark exercise, so it is tedious by nature: go through every number and paragraph, don't sample.

## What to compare against

- **Required:** the draft report.
- **Optional, any subset.** Never require all of them:
  1. The final report of the past quarter, or of the last two quarters.
  2. An internal Excel file with reporting data. Most funds have one, but not all.
  3. Word files or other documents that hold the qualitative parts, next to the Excel file with the numbers.
  4. Any other source the user wants considered, for example portfolio-company reporting that the fund report should not contradict.
- If it isn't clear which file is the draft and which are comparison sources, ask once, then proceed. Don't guess.
- Note which of the four source types were not supplied. This goes into your reply.

## What to look for

Look for anything inconsistent. Compare every number and paragraph in the draft with the other sources, and with the other places in the draft where the same thing appears.

- The same figure differs between two places in the draft, or between the draft and another source.
- A name changes, for example "Super Burger Inc" last quarter and "SuperBurger" now.
- Figures that don't fit together. A company with a MOIC of 1.4x and an IRR of -5.4% doesn't sound right, for example.

Compare like with like: same period, same basis (gross or net), same entity, same currency and units. A difference that comes from different periods or bases is not a finding, unless the draft presents them as the same thing. A difference that rounding to the displayed precision explains is not a finding either.

You flag where documents disagree. You don't decide which figure is right, and you don't reconcile against a ledger or any other authoritative source. Checking the report against the guidelines the fund has to adhere to is not part of this version.

## Method

1. **Timestamp.** Run `date -u +%Y-%m-%dT%H:%M:%SZ` once at the start and use that value for the run. Never guess the time. If you can't run it, ask the user for the date and time.
2. **First run in a folder.** Follow the Ground rules' "First run in a folder". On a genuine first run, also tell the user, in two sentences: the documents you review are sent to Anthropic to be processed in this session; nothing goes to fundcfo.ai's servers.
3. **Read every document fully.** If a file can't be read or parses badly (scanned image, garbled tables), say so plainly and never fill in numbers you couldn't read.
4. **Check** every number, name and paragraph as described above.
5. **Reply in chat**, then **log the run** to `actions.md`.

## Reply in chat

Structure the reply as a list of observations, each written like "IRR 5.4% on pg. 3 vs 5.2% on pg. 2", with one explainer sentence below it:

- **Exact findings** — concrete, citable mismatches: the same figure or name differing between two places.
- **General notes** — judgment calls, such as figures that don't fit together. Word these as "worth a look", not as errors.
- **Could not check** — what couldn't be checked and why. Omit if everything ran.

If nothing was found, say so plainly. Always say which of the four source types weren't supplied, so silence about them is never read as a clean result on those. Quote values exactly as they appear in the documents. If one underlying discrepancy shows up more than once, report it once, under the most specific heading.

## Log the run

One `actions.md` line per run (see Ground rules), after the chat reply:

`<timestamp> | Reviewed <draft file name>: <N> findings, <M> notes<, nothing to compare against if no sources were supplied>`

Example: `2026-09-22T10:20:00Z | Reviewed Q2-draft.pdf: 3 findings, 1 note`

This line is the only persisted record of the run — the observations themselves live in the chat reply, not in a file. If the user wants a run's findings kept, tell them to save that reply themselves; this skill doesn't write a findings file.

## Don't

- Don't invent findings, numbers or page references.
- Don't say which of two disagreeing figures is correct.
- Don't modify, rename, move or delete the user's documents without asking for permission first.
