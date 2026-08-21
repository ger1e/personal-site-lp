#!/usr/bin/env python3
"""Entry-point QA that understands the split static runtime."""
from pathlib import Path
import sys

from qa import audit_repository


def main() -> int:
    root = Path.cwd()
    failures = audit_repository(root)
    css = (root / "site.css").read_text(encoding="utf-8") if (root / "site.css").is_file() else ""
    resolved = {
        "index.html is missing prefers-reduced-motion support": "prefers-reduced-motion" in css,
        "index.html is missing :focus-visible keyboard focus styling": ":focus-visible" in css,
    }
    failures = [failure for failure in failures if not resolved.get(failure, False)]
    if failures:
        print("QA FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("QA PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
