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
SECURITY_TXT_URL = "https://gergoilly.hu/.well-known/security.txt"
SENTRY_INGEST = "https://o4511932881502208.ingest.de.sentry.io"
SENTRY_CDNS = ("https://js.sentry-cdn.com", "https://browser.sentry-cdn.com")
CONFLICT_LINE = re.compile(r"^(?:<<<<<<<(?: .+)?|=======|>>>>>>>(?: .+)?)\s*$", re.MULTILINE)
SENTRY_AUTH_TOKEN = re.compile(r"\bsntry[su]_[A-Za-z0-9_-]{12,}\b")
PRIVATE_KEY_HEADER = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
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


def _csp_has_broad_wildcard(csp: str) -> bool:
    for directive in csp.split(";"):
        parts = directive.strip().split()
        if parts and parts[0].casefold() in {"default-src", "script-src", "connect-src"} and "*" in parts[1:]:
            return True
    return False


def _audit_sentry_contract(root: Path, html: str, failures: list[str]) -> None:
    compact_html = re.sub(r"\s+", "", html)
    browser_requirements = {
        "sendDefaultPii:false": "browser Sentry must disable default PII",
        "replaysSessionSampleRate:0": "browser Sentry session replay must be disabled",
        "replaysOnErrorSampleRate:0": "browser Sentry error replay must be disabled",
        "deleteevent.request.cookies": "browser Sentry must strip request cookies",
        "deleteevent.request.headers": "browser Sentry must strip request headers",
        "deleteevent.request.data": "browser Sentry must strip request bodies",
    }
    for token, message in browser_requirements.items():
        if token not in compact_html:
            failures.append(message)

    meta_match = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
        html,
        re.IGNORECASE,
    )
    if not meta_match:
        failures.append("index.html is missing page-level Content-Security-Policy")
    else:
        page_csp = meta_match.group(1)
        if SENTRY_INGEST not in page_csp or any(origin not in page_csp for origin in SENTRY_CDNS):
            failures.append("index.html CSP is missing required Sentry allowlist origins")
        if _csp_has_broad_wildcard(page_csp):
            failures.append("index.html CSP contains a broad wildcard source")

    instrument = root / "instrument.js"
    if instrument.is_file():
        text = instrument.read_text(encoding="utf-8")
        compact = re.sub(r"\s+", "", text)
        server_requirements = {
            "release:process.env.VERCEL_GIT_COMMIT_SHA||undefined": "Node Sentry is missing Vercel Git release tagging",
            "enableLogs:true": "Node Sentry structured logs are disabled",
            "tracesSampleRate:isProduction?0.1:1.0": "Node Sentry production trace sampling must be 10%",
            "sendDefaultPii:false": "Node Sentry must disable default PII",
            "userInfo:false": "Node Sentry must disable user-info collection",
            "httpBodies:[]": "Node Sentry must disable HTTP-body collection",
        }
        for token, message in server_requirements.items():
            if token not in compact:
                failures.append(message)


def _audit_dependency_lock(root: Path, failures: list[str]) -> None:
    package_path = root / "package.json"
    lock_path = root / "package-lock.json"
    if not package_path.is_file():
        return
    package = _parse_json(package_path, failures)
    if not lock_path.is_file():
        failures.append("package-lock.json is missing")
        return
    lock = _parse_json(lock_path, failures)
    if not isinstance(package, dict) or not isinstance(lock, dict):
        return
    if lock.get("lockfileVersion") != 3:
        failures.append("package-lock.json must use lockfileVersion 3")
    dependencies = package.get("dependencies", {})
    expected = dependencies.get("@sentry/node") if isinstance(dependencies, dict) else None
    if not isinstance(expected, str) or not re.fullmatch(r"\d+\.\d+\.\d+", expected):
        failures.append("@sentry/node must be pinned to an exact semantic version")
        return
    packages = lock.get("packages", {})
    locked = packages.get("node_modules/@sentry/node", {}) if isinstance(packages, dict) else {}
    actual = locked.get("version") if isinstance(locked, dict) else None
    if actual != expected:
        failures.append(f"Sentry lock version mismatch: package.json={expected}, package-lock.json={actual}")


def _audit_secret_material(root: Path, failures: list[str]) -> None:
    for path in _iter_text_files(root):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] == "tests":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if SENTRY_AUTH_TOKEN.search(text):
            failures.append(f"Sentry auth token material found in {relative}")
        if PRIVATE_KEY_HEADER.search(text):
            failures.append(f"private key material found in {relative}")


def audit_repository(root: Path) -> list[str]:
    root = root.resolve()
    failures: list[str] = []
    index = root / "index.html"

    for name in [
        "README.md", "index.html", "403.html", "404.html", "robots.txt", "sitemap.xml",
        "site.webmanifest", "vercel.json", "favicon.svg", "favicon.ico", "og-card.png",
        ".well-known/security.txt", "security.txt", "package.json", "package-lock.json", "instrument.js",
    ]:
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

    _audit_sentry_contract(root, html, failures)
    _audit_dependency_lock(root, failures)

    vercel = _parse_json(root / "vercel.json", failures) if (root / "vercel.json").is_file() else None
    if isinstance(vercel, dict):
        routes = vercel.get("routes")
        if not isinstance(routes, list):
            failures.append("vercel.json is missing routes")
        else:
            serialized = json.dumps(routes)
            if "Content-Security-Policy" not in serialized or "frame-ancestors 'none'" not in serialized:
                failures.append("vercel.json is missing hardened Content-Security-Policy headers")
            csp_values = [
                headers.get("Content-Security-Policy")
                for route in routes if isinstance(route, dict)
                for headers in [route.get("headers", {})]
                if isinstance(headers, dict) and isinstance(headers.get("Content-Security-Policy"), str)
            ]
            if not csp_values:
                failures.append("vercel.json is missing Content-Security-Policy")
            else:
                csp = csp_values[0]
                if SENTRY_INGEST not in csp or any(origin not in csp for origin in SENTRY_CDNS):
                    failures.append("vercel.json Sentry CSP allowlist is incomplete")
                if _csp_has_broad_wildcard(csp):
                    failures.append("vercel.json CSP contains a broad wildcard source")
            if not any(isinstance(r, dict) and r.get("handle") == "filesystem" for r in routes):
                failures.append("vercel.json is missing filesystem routing guard")
            if not any(isinstance(r, dict) and r.get("dest") == "/api/404" and r.get("src") == "/(.*)" for r in routes):
                failures.append("vercel.json is missing catch-all custom 404 routing")
            if not any(isinstance(r, dict) and r.get("dest") == "/api/403" for r in routes):
                failures.append("vercel.json is missing custom 403 routing")
            for security_path in ("/.well-known/security.txt", "/security.txt"):
                if not any(isinstance(r, dict) and r.get("src") == security_path and "text/plain" in json.dumps(r.get("headers", {})) for r in routes):
                    failures.append(f"vercel.json is missing text/plain headers for {security_path}")

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

    canonical_security = root / ".well-known/security.txt"
    compatibility_security = root / "security.txt"
    if canonical_security.is_file():
        sec = canonical_security.read_text(encoding="utf-8")
        for field in ("Contact:", "Expires:", "Canonical:", "Policy:"):
            if not re.search(rf"(?m)^{re.escape(field)}\s+\S+", sec):
                failures.append(f".well-known/security.txt is missing {field[:-1]}")
        if f"Canonical: {SECURITY_TXT_URL}" not in sec:
            failures.append(".well-known/security.txt has incorrect Canonical URL")
        if "Preferred-Languages: en, hu" not in sec:
            failures.append(".well-known/security.txt is missing preferred languages")
        if compatibility_security.is_file() and compatibility_security.read_text(encoding="utf-8") != sec:
            failures.append("security.txt compatibility copy differs from canonical security.txt")

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

    _audit_secret_material(root, failures)

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
