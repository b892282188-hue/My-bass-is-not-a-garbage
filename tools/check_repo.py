#!/usr/bin/env python3
"""Repository hygiene checks. Run locally and in CI with: python tools/check_repo.py

Checks:
1. Relative links in Markdown files point to files that exist.
2. No audio files are tracked outside tests/fixtures/real/ (ENGINEERING_RULES 8, 25).
3. tests/fixtures/real/ stays under the agreed size cap.
4. No open-source license file is present (ENGINEERING_RULES 26).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO_EXTS = {".wav", ".aif", ".aiff", ".flac", ".mp3", ".m4a", ".ogg", ".caf"}
FIXTURE_DIR = "tests/fixtures/real/"
FIXTURE_CAP_BYTES = 20 * 1024 * 1024
LICENSE_NAMES = {"license", "license.md", "license.txt", "copying", "copying.md", "copying.txt"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
# Archived third-party documents are kept verbatim and not link-checked.
LINK_CHECK_EXCLUDE = ("docs/research/",)


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
    ).stdout.decode("utf-8")
    return [p for p in out.split("\0") if p]


def check_links(files: list[str]) -> list[str]:
    errors = []
    for rel in files:
        if not rel.endswith(".md") or rel.startswith(LINK_CHECK_EXCLUDE):
            continue
        text = FENCE_RE.sub("", (ROOT / rel).read_text(encoding="utf-8"))
        for target in LINK_RE.findall(text):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0]
            if not path:
                continue
            if not (ROOT / rel).parent.joinpath(path).exists():
                errors.append(f"{rel}: broken link -> {target}")
    return errors


def check_audio(files: list[str]) -> list[str]:
    errors = []
    fixture_bytes = 0
    for rel in files:
        if Path(rel).suffix.lower() not in AUDIO_EXTS:
            continue
        if rel.startswith(FIXTURE_DIR):
            fixture_bytes += (ROOT / rel).stat().st_size
        else:
            errors.append(f"{rel}: audio file outside {FIXTURE_DIR}")
    if fixture_bytes > FIXTURE_CAP_BYTES:
        errors.append(
            f"{FIXTURE_DIR}: {fixture_bytes} bytes exceeds cap of {FIXTURE_CAP_BYTES}"
        )
    return errors


def check_license(files: list[str]) -> list[str]:
    return [
        f"{rel}: license files must not be added (see docs/adr/ADR-008)"
        for rel in files
        if "/" not in rel and rel.lower() in LICENSE_NAMES
    ]


def main() -> int:
    files = tracked_files()
    errors = check_links(files) + check_audio(files) + check_license(files)
    for err in errors:
        print(f"ERROR {err}")
    print(f"checked {len(files)} tracked files, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
