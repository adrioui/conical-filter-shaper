#!/usr/bin/env python3
"""
Bump the design revision.

Actions:
  1. Updates cad/params.py  REVISION = "X.Y"
  2. Appends entry to CHANGELOG.md
  3. Prints reminder to re-run build_exports.py and gen_bom.py

Usage:
    python scripts/bump_revision.py 0.2 "Short description of what changed"
"""
from __future__ import annotations
import sys
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
PARAMS_FILE = ROOT / "cad" / "params.py"
CHANGELOG = ROOT / "CHANGELOG.md"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: bump_revision.py <new_revision> [description]")
        sys.exit(1)

    new_rev = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else "Design revision bump"
    today = date.today().isoformat()

    # ── Update params.py ──────────────────────────────────────────────────────
    text = PARAMS_FILE.read_text()
    old_rev_match = re.search(r'REVISION: Final\[str\] = "([^"]+)"', text)
    if not old_rev_match:
        print("ERROR: Could not find REVISION in params.py")
        sys.exit(1)
    old_rev = old_rev_match.group(1)
    text = text.replace(
        f'REVISION: Final[str] = "{old_rev}"',
        f'REVISION: Final[str] = "{new_rev}"',
    )
    PARAMS_FILE.write_text(text)
    print(f"  ✅ params.py: {old_rev} → {new_rev}")

    # ── Update CHANGELOG.md ────────────────────────────────────────────────────
    entry = f"\n## [{new_rev}] {today} — {description}\n\n- (add details here)\n"
    changelog_text = CHANGELOG.read_text()
    insert_after = "<!-- bump_revision.py appends entries above this line -->"
    changelog_text = changelog_text.replace(insert_after, entry + "\n---\n\n" + insert_after)
    CHANGELOG.write_text(changelog_text)
    print(f"  ✅ CHANGELOG.md: entry added for [{new_rev}]")

    # ── Reminder ───────────────────────────────────────────────────────────────
    print(f"\n  Next steps:")
    print(f"    pytest tests/ -v")
    print(f"    python scripts/build_exports.py")
    print(f"    python scripts/gen_bom.py")
    print(f"    git add cad/params.py CHANGELOG.md")
    print(f"    git commit -m 'bump revision to {new_rev}: {description}'")
    print(f"    git tag v{new_rev}")


if __name__ == "__main__":
    main()
