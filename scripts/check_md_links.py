#!/usr/bin/env python3
"""Check that every relative Markdown link in tracked *.md files resolves. Exit 1 on broken links."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"```.*?```", re.S)


def main() -> int:
    files = subprocess.run(["git", "ls-files", "*.md"], capture_output=True, text=True, check=True).stdout.split()
    broken = 0
    for f in files:
        text = FENCE.sub("", Path(f).read_text(encoding="utf-8", errors="replace"))
        for target in LINK.findall(text):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
                continue
            path = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if path and not (Path(f).parent / path).exists():
                print(f"{f}: {target}")
                broken += 1
    print(f"{broken} broken link(s) in {len(files)} markdown files")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
