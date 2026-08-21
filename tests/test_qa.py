from pathlib import Path
import json
import tempfile
import unittest

from scripts.qa import audit_repository

SENTRY_INGEST = "https://o4511932881502208.ingest.de.sentry.io"
SENTRY_DSN = "https://d21115d9c71acb4ba224be1fe334460f@o4511932881502208.ingest.de.sentry.io/4511947440259152"
SENTRY_CSP = (
    "default-src 'none'; style-src 'self' 'unsafe-inline'; "
    "script-src 'unsafe-inline' https://js.sentry-cdn.com https://browser.sentry-cdn.com; "
    f"connect-src 'self' {SENTRY_INGEST}; object-src 'none'; base-uri 'none'; "
    "form-action 'none'; frame-ancestors 'none'"
)

VALID_HTML = f'''<!doctype html><html><head>
<link rel="canonical" href="https://gergoilly.hu/">
<meta property="og:image" content="https://gergoilly.hu/og-card.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="manifest" href="/site.webmanifest">
<script type="application/ld+json">{{}}</script>
<meta http-equiv="Content-Security-Policy" content="{SENTRY_CSP}">
<script>window.sentryOnLoad=function(){{Sentry.init({{dsn:"{SENTRY_DSN}",tracesSampleRate:0.1,sendDefaultPii:false,replaysSessionSampleRate:0,replaysOnErrorSampleRate:0,beforeSend(event){{if(event.request){{delete event.request.cookies;delete event.request.headers;delete event.request.data;}}return event;}}}});}};</script>
<script src="https://js.sentry-cdn.com/d21115d9c71acb4ba224be1fe334460f.min.js"></script>
<style>:focus-visible{{outline:2px solid currentColor}}@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>
</head><body><img src="/favicon.svg" alt="fixture"></body></html>'''

PNG = b"\x89PNG\r\n\x1a\nfixture"
ICO = b"\x00\x00\x01\x00fixture"
SECURITY_TXT = """Contact: https://github.com/ger1e
Expires: 2027-08-21T00:00:00Z
Preferred-Languages: en, hu
Canonical: https://gergoilly.hu/.well-known/security.txt
Policy: https://github.com/ger1e/personal-site-lp/security/policy
"""

PACKAGE_JSON = {
    "name": "fixture",
    "version": "1.0.0",
    "private": True,
    "dependencies": {"@sentry/node": "10.70.0"},
}
PACKAGE_LOCK = {
    "name": "fixture",
    "version": "1.0.0",
    "lockfileVersion": 3,
    "requires": True,
    "packages": {
        "": {
            "name": "fixture",
            "version": "1.0.0",
            "dependencies": {"@sentry/node": "10.70.0"},
        },
        "node_modules/@sentry/node": {"version": "10.70.0"},
    },
}
INSTRUMENT_JS = f'''const Sentry = require("@sentry/node");
Sentry.init({{
  dsn: process.env.SENTRY_DSN || "{SENTRY_DSN}",
  environment: process.env.VERCEL_ENV || process.env.NODE_ENV || "development",
  release: process.env.VERCEL_GIT_COMMIT_SHA || undefined,
  enableLogs: true,
  tracesSampleRate: 0.1,
  sendDefaultPii: false,
  dataCollection: {{ userInfo: false, httpBodies: [] }},
}});
module.exports = Sentry;
'''


class RepositoryAuditTests(unittest.TestCase):
    def make_repo(self, html: str = VALID_HTML) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "api").mkdir()
        (root / ".well-known").mkdir()
        (root / "README.md").write_text("# fixture\n", encoding="utf-8")
        (root / "index.html").write_text(html, encoding="utf-8")
        (root / "package.json").write_text(json.dumps(PACKAGE_JSON), encoding="utf-8")
        (root / "package-lock.json").write_text(json.dumps(PACKAGE_LOCK), encoding="utf-8")
        (root / "instrument.js").write_text(INSTRUMENT_JS, encoding="utf-8")
        handler = """module.exports=async(req,res)=>{res.statusCode=STATUS;res.setHeader('Content-Type','text/html; charset=utf-8');res.setHeader('Cache-Control','public, max-age=0, must-revalidate');res.setHeader('X-Robots-Tag','noindex, nofollow');res.end('<html>STATUS</html>')}\n"""
        for code in (403, 404):
            (root / f"{code}.html").write_text(
                f'<!doctype html><html><head><meta name="robots" content="noindex,nofollow"></head><body><h1>{code}</h1><a href="/">home</a></body></html>',
                encoding="utf-8",
            )
            (root / "api" / f"{code}.js").write_text(handler.replace("STATUS", str(code)), encoding="utf-8")
        (root / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>', encoding="utf-8")
        for name in [
            "og-card.png",
            "favicon-16x16.png",
            "favicon-32x32.png",
            "apple-touch-icon.png",
            "android-chrome-192x192.png",
            "android-chrome-512x512.png",
        ]:
            (root / name).write_bytes(PNG)
        (root / "favicon.ico").write_bytes(ICO)
        (root / "robots.txt").write_text(
            "User-agent: *\nAllow: /\nSitemap: https://gergoilly.hu/sitemap.xml\n",
            encoding="utf-8",
        )
        (root / "sitemap.xml").write_text(
            "<urlset><url><loc>https://gergoilly.hu/</loc></url></urlset>",
            encoding="utf-8",
        )
        (root / "site.webmanifest").write_text(
            json.dumps(
                {
                    "start_url": "/",
                    "display": "standalone",
                    "icons": [
                        {"src": "/android-chrome-192x192.png", "sizes": "192x192"},
                        {"src": "/android-chrome-512x512.png", "sizes": "512x512"},
                    ],
                }
            ),
            encoding="utf-8",
        )
        (root / ".well-known" / "security.txt").write_text(SECURITY_TXT, encoding="utf-8")
        (root / "security.txt").write_text(SECURITY_TXT, encoding="utf-8")
        (root / "vercel.json").write_text(
            json.dumps(
                {
                    "routes": [
                        {
                            "src": "/(.*)",
                            "headers": {"Content-Security-Policy": SENTRY_CSP},
                            "continue": True,
                        },
                        {"src": "/.well-known/security.txt", "headers": {"Content-Type": "text/plain; charset=utf-8"}, "continue": True},
                        {"src": "/security.txt", "headers": {"Content-Type": "text/plain; charset=utf-8"}, "continue": True},
                        {"src": "/403", "dest": "/api/403"},
                        {"handle": "filesystem"},
                        {"src": "/(.*)", "dest": "/api/404"},
                    ]
                }
            ),
            encoding="utf-8",
        )
        return root

    def test_valid_repository_has_no_failures(self):
        self.assertEqual(audit_repository(self.make_repo()), [])

    def test_missing_canonical_is_reported(self):
        root = self.make_repo(VALID_HTML.replace('<link rel="canonical" href="https://gergoilly.hu/">', ""))
        self.assertTrue(any("canonical" in failure.lower() for failure in audit_repository(root)))

    def test_missing_csp_header_is_reported(self):
        root = self.make_repo()
        (root / "vercel.json").write_text(
            json.dumps({"routes": [{"handle": "filesystem"}, {"src": "/(.*)", "dest": "/api/404"}]}),
            encoding="utf-8",
        )
        self.assertTrue(any("content-security-policy" in failure.lower() for failure in audit_repository(root)))

    def test_missing_local_asset_is_reported(self):
        root = self.make_repo(VALID_HTML.replace("/favicon.svg", "/missing.svg"))
        self.assertTrue(any("missing.svg" in failure for failure in audit_repository(root)))

    def test_committed_env_file_is_reported(self):
        root = self.make_repo()
        (root / ".env").write_text("SECRET=x\n", encoding="utf-8")
        self.assertTrue(any(".env" in failure for failure in audit_repository(root)))

    def test_merge_conflict_marker_is_reported(self):
        root = self.make_repo()
        (root / "notes.md").write_text("<<<<<<< HEAD\n", encoding="utf-8")
        self.assertTrue(any("merge-conflict" in failure.lower() for failure in audit_repository(root)))

    def test_security_txt_canonical_mismatch_is_reported(self):
        root = self.make_repo()
        bad = SECURITY_TXT.replace(
            "Canonical: https://gergoilly.hu/.well-known/security.txt",
            "Canonical: https://example.com/security.txt",
        )
        (root / ".well-known" / "security.txt").write_text(bad, encoding="utf-8")
        (root / "security.txt").write_text(bad, encoding="utf-8")
        self.assertTrue(any("security.txt has incorrect canonical" in failure.lower() for failure in audit_repository(root)))

    def test_missing_package_lock_is_reported(self):
        root = self.make_repo()
        (root / "package-lock.json").unlink()
        self.assertTrue(any("package-lock" in failure.lower() for failure in audit_repository(root)))

    def test_mismatched_sentry_lock_version_is_reported(self):
        root = self.make_repo()
        lock = PACKAGE_LOCK | {
            "packages": PACKAGE_LOCK["packages"] | {
                "node_modules/@sentry/node": {"version": "10.69.0"}
            }
        }
        (root / "package-lock.json").write_text(json.dumps(lock), encoding="utf-8")
        self.assertTrue(any("sentry" in failure.lower() and "version" in failure.lower() for failure in audit_repository(root)))

    def test_missing_sentry_ingest_allowlist_is_reported(self):
        root = self.make_repo()
        config = json.loads((root / "vercel.json").read_text(encoding="utf-8"))
        config["routes"][0]["headers"]["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        (root / "vercel.json").write_text(json.dumps(config), encoding="utf-8")
        self.assertTrue(any("sentry" in failure.lower() and "csp" in failure.lower() for failure in audit_repository(root)))

    def test_wildcard_csp_source_is_reported(self):
        root = self.make_repo()
        config = json.loads((root / "vercel.json").read_text(encoding="utf-8"))
        config["routes"][0]["headers"]["Content-Security-Policy"] = (
            "default-src 'none'; script-src * 'unsafe-inline'; connect-src *; frame-ancestors 'none'"
        )
        (root / "vercel.json").write_text(json.dumps(config), encoding="utf-8")
        self.assertTrue(any("wildcard" in failure.lower() for failure in audit_repository(root)))

    def test_sentry_auth_token_is_reported_but_public_dsn_is_allowed(self):
        root = self.make_repo()
        (root / "notes.md").write_text(f"PUBLIC_DSN={SENTRY_DSN}\nSENTRY_AUTH_TOKEN=sntryu_example_secret_material\n", encoding="utf-8")
        failures = audit_repository(root)
        self.assertTrue(any("sentry auth token" in failure.lower() for failure in failures))
        self.assertFalse(any("public_dsn" in failure.lower() for failure in failures))

    def test_private_key_header_is_reported(self):
        root = self.make_repo()
        (root / "notes.md").write_text("-----BEGIN PRIVATE KEY-----\n", encoding="utf-8")
        self.assertTrue(any("private key" in failure.lower() for failure in audit_repository(root)))


if __name__ == "__main__":
    unittest.main()
