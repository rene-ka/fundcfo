#!/usr/bin/env python3
"""Copy the Ground rules block from OPERATING-RULES.md into every skill's
SKILL.md, between the <!-- OPERATING-RULES:START --> and
<!-- OPERATING-RULES:END --> markers.

Run from the repo root:

    python3 scripts/sync-operating-rules.py

OPERATING-RULES.md is the single source of truth. Everything from its
"## Ground rules" heading to the end of the file is copied verbatim into
every skills/*/SKILL.md that has both markers. A skill file with no markers
is left alone and reported as skipped — add the markers to that file first
if it should carry the ground rules too.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "OPERATING-RULES.md"
START = "<!-- OPERATING-RULES:START -->"
END = "<!-- OPERATING-RULES:END -->"
HEADING = "## Ground rules"


def extract_block(text: str) -> str:
    # Match the heading only as its own line, not an incidental mention
    # elsewhere in the file (e.g. a backtick-quoted reference to it in prose).
    match = re.search(rf"^{re.escape(HEADING)}\s*$", text, re.MULTILINE)
    if match is None:
        sys.exit(f"error: {SOURCE.name} has no '{HEADING}' heading on its own line")
    return text[match.start():].rstrip("\n") + "\n"


def main() -> None:
    if not SOURCE.exists():
        sys.exit(f"error: {SOURCE} not found")

    block = extract_block(SOURCE.read_text())
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    replacement = START + "\n" + block + END

    changed, unchanged, skipped = [], [], []
    for skill_md in sorted(ROOT.glob("skills/*/SKILL.md")):
        text = skill_md.read_text()
        if START not in text or END not in text:
            skipped.append(skill_md)
            continue
        new_text = pattern.sub(replacement, text)
        if new_text != text:
            skill_md.write_text(new_text)
            changed.append(skill_md)
        else:
            unchanged.append(skill_md)

    for f in changed:
        print(f"updated:   {f.relative_to(ROOT)}")
    for f in unchanged:
        print(f"unchanged: {f.relative_to(ROOT)}")
    for f in skipped:
        print(f"skipped (no markers): {f.relative_to(ROOT)}")
    if not changed and not unchanged and not skipped:
        print("no skill files found under skills/*/SKILL.md")


if __name__ == "__main__":
    main()
