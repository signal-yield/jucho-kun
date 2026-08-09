from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "jucho-kun"
DESTINATION = ROOT / "plugins" / "jucho-kun" / "skills" / "jucho-kun"


def matches() -> bool:
    if not DESTINATION.is_dir():
        return False
    comparison = filecmp.dircmp(SOURCE, DESTINATION)
    return not (
        comparison.left_only
        or comparison.right_only
        or comparison.diff_files
        or comparison.funny_files
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        if matches():
            return 0
        print("Codex packaged skill differs from skills/jucho-kun", file=sys.stderr)
        return 1

    if DESTINATION.exists():
        shutil.rmtree(DESTINATION)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, DESTINATION)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
