import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicPrivacyContractTests(unittest.TestCase):
    def test_public_surface_minimizes_identity_and_employer_metadata(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        js = (ROOT / "site.js").read_text(encoding="utf-8")
        public = f"{html}\n{js}"
        lowered = public.casefold()

        for forbidden in (
            "budapest",
            "europe/budapest",
            "addresslocality",
            "mailto:",
            "mail@gergoilly.hu",
            "+36 30 732 0566",
            "simple-icons",
            "ibm consulting",
            "ibm-logo",
            'alt="ibm"',
            "black hoodie at a metro station",
        ):
            self.assertNotIn(forbidden, lowered)

        # Preserve useful professional proof-of-work and canonical identity anchors.
        self.assertIn("cyber threat hunter", lowered)
        self.assertIn("https://linkedin.com/in/gergoilly", lowered)
        self.assertIn("https://gergoilly.hu/", lowered)
        self.assertIn("https://github.com/ger1e", lowered)


if __name__ == "__main__":
    unittest.main()
