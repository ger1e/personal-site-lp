#!/usr/bin/env python3
"""Dependency-free structural QA for the static personal site."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}


class _ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.references.append((name, value.strip()))



def _is_local_reference(value: str) -> bool:
    if not value or value.startswith("#"):
        return False
    parsed = urlsplit(value)
    return not parsed.scheme and not parsed.netloc



def _resolve_local_reference(root: Path, source: Path, value: str) -> Path | None:
    parsed = urlsplit(value)
    path_text = unquote(parsed.path)
    if not path_text:
        return None

    if path_text.startswith("/"):
        candidate = root / path_text.lstrip("/")
    else:
        candidate = source.parent / path_text

    try:
        resolved = candidate.resolve()
        resolved.relative_to(root.resolve())
    except (OSError, ValueError):
        return None
    return resolved



def _iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {".editorconfig", ".gitattributes", ".gitignore"}:
            yield path



def audit_repository(root: Path) -> list[str]:
    """Return human-readable structural QA failures for *root*."""
    root = root.resolve()
    failures: list[str] = []

    readme = root / "README.md"
    index = root / "index.html"

    if not readme.is_file():
        failures.append("README.md is missing")

    if not index.is_file():
        failures.append("index.html is missing")
        return failures

    try:
        html = index.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        failures.append(f"index.html cannot be read as UTF-8: {exc}")
        return failures

    if not html.strip():
        failures.append("index.html is empty")
        return failures

    lowered = html.casefold()
    required_tokens = {
        "<!doctype html": "doctype declaration",
        "<html": "<html element",
        "<head": "<head element",
        "<body": "<body element",
        "content-security-policy": "Content-Security-Policy meta tag",
        "prefers-reduced-motion": "prefers-reduced-motion support",
        ":focus-visible": ":focus-visible keyboard focus styling",
    }
    for token, description in required_tokens.items():
        if token not in lowered:
            failures.append(f"index.html is missing {description}")

    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.name.startswith(".env") and path.name != ".env.example":
            failures.append(f"committed environment file is forbidden: {path.relative_to(root)}")

    for path in _iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if any(marker in text for marker in CONFLICT_MARKERS):
            failures.append(f"merge-conflict marker found in {path.relative_to(root)}")

    parser = _ReferenceParser()
    try:
        parser.feed(html)
    except Exception as exc:  # HTMLParser is permissive; retain a useful audit failure if it does fail.
        failures.append(f"index.html could not be parsed: {exc}")
        return failures

    for attribute, value in parser.references:
        if not _is_local_reference(value):
            continue
        target = _resolve_local_reference(root, index, value)
        if target is None:
            failures.append(f"unsafe local {attribute} reference: {value}")
        elif not target.exists():
            failures.append(f"missing local asset referenced by {attribute}: {value}")

    return failures



def main() -> int:
    failures = audit_repository(Path.cwd())
    if failures:
        print("QA FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("QA PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
