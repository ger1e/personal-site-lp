import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicPrivacyContractTests(unittest.TestCase):
    def test_homepage_minimizes_machine_readable_identity(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        lowered = html.casefold()

        self.assertNotIn("budapest", lowered)
        self.assertNotIn("addresslocality", lowered)
        self.assertNotIn("mailto:", lowered)
        self.assertNotIn("simple-icons", lowered)
        self.assertNotIn('alt="ibm"', lowered)
        self.assertNotIn("black hoodie at a metro station", lowered)

        # Preserve useful professional proof-of-work and canonical identity anchors.
        self.assertIn("cyber threat hunter", lowered)
        self.assertIn("https://linkedin.com/in/gergoilly", lowered)
        self.assertIn("https://gergoilly.hu/", lowered)


if __name__ == "__main__":
    unittest.main()
