from pathlib import Path
import json
import tempfile
import unittest

from scripts.qa import audit_repository

VALID_HTML = '''<!doctype html><html><head>
<link rel="canonical" href="https://gergoilly.hu/">
<meta property="og:image" content="https://gergoilly.hu/og-card.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="manifest" href="/site.webmanifest">
<script type="application/ld+json">{}</script>
<style>:focus-visible{outline:2px solid currentColor}@media (prefers-reduced-motion: reduce){*{animation:none!important}}</style>
</head><body><img src="/favicon.svg" alt="fixture"></body></html>'''

PNG = b"\x89PNG\r\n\x1a\nfixture"
ICO = b"\x00\x00\x01\x00fixture"
SECURITY_TXT = """Contact: https://github.com/ger1e
Expires: 2027-08-21T00:00:00Z
Preferred-Languages: en, hu
Canonical: https://gergoilly.hu/.well-known/security.txt
Policy: https://github.com/ger1e/personal-site-lp/security/policy
"""


class RepositoryAuditTests(unittest.TestCase):
    def make_repo(self, html: str = VALID_HTML) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "api").mkdir()
        (root / ".well-known").mkdir()
        (root / "README.md").write_text("# fixture\n", encoding="utf-8")
        (root / "index.html").write_text(html, encoding="utf-8")
        for code in (403, 404):
            (root / f"{code}.html").write_text(
                f'<!doctype html><html><head><meta name="robots" content="noindex,nofollow"></head><body><h1>{code}</h1><a href="/">home</a></body></html>',
                encoding="utf-8",
            )
            (root / "api" / f"{code}.js").write_text("module.exports=()=>{}\n", encoding="utf-8")
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
                            "headers": {"Content-Security-Policy": "frame-ancestors 'none'"},
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


if __name__ == "__main__":
    unittest.main()
