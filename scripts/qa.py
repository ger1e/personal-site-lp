#!/usr/bin/env python3
"""Dependency-free production QA for the static personal site."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote, urlsplit

CANONICAL_URL = "https://gergoilly.hu/"
CONFLICT_LINE = re.compile(r"^(?:<<<<<<<(?: .+)?|=======|>>>>>>>(?: .+)?)\s*$", re.MULTILINE)
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".md", ".py", ".txt", ".xml", ".yaml", ".yml", ".webmanifest"}


class _ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.references.append((name, value.strip()))


def _is_local_reference(value: str) -> bool:
    if not value or value.startswith("#") or value.startswith("data:"):
        return False
    parsed = urlsplit(value)
    return not parsed.scheme and not parsed.netloc


def _resolve_local_reference(root: Path, source: Path, value: str) -> Path | None:
    parsed = urlsplit(value)
    path_text = unquote(parsed.path)
    if not path_text:
        return None
    candidate = root / path_text.lstrip("/") if path_text.startswith("/") else source.parent / path_text
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


def _parse_json(path: Path, failures: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        failures.append(f"{path.name} is invalid: {exc}")
        return None


def _audit_html_references(root: Path, source: Path, failures: list[str]) -> None:
    try:
        html = source.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        failures.append(f"{source.name} cannot be read as UTF-8: {exc}")
        return
    parser = _ReferenceParser()
    try:
        parser.feed(html)
    except Exception as exc:
        failures.append(f"{source.name} could not be parsed: {exc}")
        return
    for attribute, value in parser.references:
        if not _is_local_reference(value):
            continue
        target = _resolve_local_reference(root, source, value)
        if target is None:
            failures.append(f"unsafe local {attribute} reference in {source.name}: {value}")
        elif not target.exists():
            failures.append(f"missing local asset referenced by {source.name} {attribute}: {value}")


def audit_repository(root: Path) -> list[str]:
    root = root.resolve()
    failures: list[str] = []
    index = root / "index.html"

    for name in ["README.md", "index.html", "403.html", "404.html", "robots.txt", "sitemap.xml", "site.webmanifest", "vercel.json", "favicon.svg", "favicon.ico", "og-card.png"]:
        if not (root / name).is_file():
            failures.append(f"{name} is missing")

    for name in ["api/403.js", "api/404.js", "apple-touch-icon.png", "android-chrome-192x192.png", "android-chrome-512x512.png"]:
        if not (root / name).is_file():
            failures.append(f"{name} is missing")

    if not index.is_file():
        return failures
    try:
        html = index.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        failures.append(f"index.html cannot be read as UTF-8: {exc}")
        return failures
    lowered = html.casefold()
    required_tokens = {
        "<!doctype html": "doctype declaration",
        "<head": "<head element",
        "<body": "<body element",
        'rel="canonical" href="https://gergoilly.hu/"': "canonical URL",
        'property="og:image" content="https://gergoilly.hu/og-card.png"': "Open Graph image",
        'name="twitter:card" content="summary_large_image"': "Twitter large-card metadata",
        'rel="manifest" href="/site.webmanifest"': "web app manifest",
        "application/ld+json": "JSON-LD structured data",
        "prefers-reduced-motion": "prefers-reduced-motion support",
        ":focus-visible": ":focus-visible keyboard focus styling",
    }
    for token, description in required_tokens.items():
        if token not in lowered:
            failures.append(f"index.html is missing {description}")

    vercel = _parse_json(root / "vercel.json", failures) if (root / "vercel.json").is_file() else None
    if isinstance(vercel, dict):
        routes = vercel.get("routes")
        if not isinstance(routes, list):
            failures.append("vercel.json is missing routes")
        else:
            serialized = json.dumps(routes)
            if "Content-Security-Policy" not in serialized or "frame-ancestors 'none'" not in serialized:
                failures.append("vercel.json is missing hardened Content-Security-Policy headers")
            if not any(isinstance(r, dict) and r.get("handle") == "filesystem" for r in routes):
                failures.append("vercel.json is missing filesystem routing guard")
            if not any(isinstance(r, dict) and r.get("dest") == "/api/404" and r.get("src") == "/(.*)" for r in routes):
                failures.append("vercel.json is missing catch-all custom 404 routing")
            if not any(isinstance(r, dict) and r.get("dest") == "/api/403" for r in routes):
                failures.append("vercel.json is missing custom 403 routing")

    manifest = _parse_json(root / "site.webmanifest", failures) if (root / "site.webmanifest").is_file() else None
    if isinstance(manifest, dict):
        if manifest.get("start_url") != "/" or manifest.get("display") != "standalone":
            failures.append("site.webmanifest has invalid start_url/display")
        icons = manifest.get("icons", [])
        for required_size in {"192x192", "512x512"}:
            if not any(isinstance(icon, dict) and icon.get("sizes") == required_size for icon in icons):
                failures.append(f"site.webmanifest is missing {required_size} icon")

    if (root / "robots.txt").is_file():
        robots = (root / "robots.txt").read_text(encoding="utf-8")
        if f"Sitemap: {CANONICAL_URL}sitemap.xml" not in robots:
            failures.append("robots.txt is missing canonical sitemap URL")
    if (root / "sitemap.xml").is_file():
        sitemap = (root / "sitemap.xml").read_text(encoding="utf-8")
        if f"<loc>{CANONICAL_URL}</loc>" not in sitemap:
            failures.append("sitemap.xml is missing canonical homepage URL")

    for code in (403, 404):
        path = root / f"{code}.html"
        if path.is_file():
            text = path.read_text(encoding="utf-8").casefold()
            if f">{code}<" not in text or 'name="robots" content="noindex,nofollow"' not in text:
                failures.append(f"{code}.html is missing status branding or noindex metadata")

    for png_name in ["og-card.png", "favicon-16x16.png", "favicon-32x32.png", "apple-touch-icon.png", "android-chrome-192x192.png", "android-chrome-512x512.png"]:
        path = root / png_name
        if path.is_file() and path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            failures.append(f"{png_name} is not a valid PNG signature")
    ico = root / "favicon.ico"
    if ico.is_file() and ico.read_bytes()[:4] != b"\x00\x00\x01\x00":
        failures.append("favicon.ico has an invalid ICO signature")

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
        if CONFLICT_LINE.search(text):
            failures.append(f"merge-conflict marker found in {path.relative_to(root)}")

    for source in [index, root / "403.html", root / "404.html"]:
        if source.is_file():
            _audit_html_references(root, source, failures)

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
