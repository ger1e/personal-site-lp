from pathlib import Path
import tempfile
import unittest

from scripts.qa import audit_repository


VALID_HTML = """<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self'\">
<style>
:focus-visible { outline: 2px solid currentColor; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
</style>
</head>
<body><img src=\"asset.svg\" alt=\"fixture\"></body>
</html>
"""


class RepositoryAuditTests(unittest.TestCase):
    def make_repo(self, html: str = VALID_HTML) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "README.md").write_text("# fixture\n", encoding="utf-8")
        (root / "index.html").write_text(html, encoding="utf-8")
        (root / "asset.svg").write_text("<svg xmlns='http://www.w3.org/2000/svg'></svg>\n", encoding="utf-8")
        return root

    def test_valid_repository_has_no_failures(self):
        self.assertEqual(audit_repository(self.make_repo()), [])

    def test_missing_html_structure_is_reported(self):
        root = self.make_repo("<html><body>broken</body></html>")
        failures = audit_repository(root)
        self.assertTrue(any("doctype" in failure.lower() for failure in failures))
        self.assertTrue(any("<head" in failure.lower() for failure in failures))

    def test_merge_conflict_marker_is_reported(self):
        root = self.make_repo(VALID_HTML + "\n<<<<<<< HEAD\n")
        failures = audit_repository(root)
        self.assertTrue(any("merge-conflict" in failure.lower() for failure in failures))

    def test_committed_env_file_is_reported(self):
        root = self.make_repo()
        (root / ".env").write_text("SECRET=do-not-commit\n", encoding="utf-8")
        failures = audit_repository(root)
        self.assertTrue(any(".env" in failure for failure in failures))

    def test_missing_local_asset_is_reported(self):
        root = self.make_repo(VALID_HTML.replace("asset.svg", "missing.svg"))
        failures = audit_repository(root)
        self.assertTrue(any("missing.svg" in failure for failure in failures))

    def test_external_and_fragment_links_are_ignored(self):
        html = VALID_HTML.replace(
            "</body>",
            '<a href="https://example.com/x">external</a><a href="#local">fragment</a></body>',
        )
        self.assertEqual(audit_repository(self.make_repo(html)), [])


if __name__ == "__main__":
    unittest.main()
