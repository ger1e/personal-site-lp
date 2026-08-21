from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"
ASSET = ROOT / "assets" / "rotund-operator-4k.avif"


class CyberpunkMaxContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_brand_and_controls(self):
        for token in (
            "ム乇 尺 1 乇",
            "CIGANY.EXE",
            "HUNT /",
            "CTI",
            "/ DETECT",
            "Behavior. Evidence. Signal.",
            "ACCESS GIT",
        ):
            self.assertIn(token, self.html)
        self.assertIn('class="sound-link"', self.html)
        self.assertNotIn("<iframe", self.html)

    def test_matrix_glitch_and_cursor(self):
        self.assertIn("const MATRIX_SPEED=3", self.html)
        for token in ("glitchline", "glitchburst", "chromashift", "panelJolt", "gridRush"):
            self.assertIn(token, self.html)
        self.assertIn("polygon points='3,3 29,15 13,20'", self.html)
        self.assertIn('rel="icon" type="image/svg+xml" href="data:image/svg+xml', self.html)

    def test_hero_asset(self):
        self.assertIn('src="assets/rotund-operator-4k.avif"', self.html)
        raw = ASSET.read_bytes()
        self.assertGreater(len(raw), 100_000)
        self.assertEqual(raw[4:8], b"ftyp")

    def test_accessibility_and_no_bootstrap(self):
        for token in (":focus-visible", "prefers-reduced-motion:reduce", "@media(pointer:coarse)"):
            self.assertIn(token, self.html)
        self.assertNotIn("raw.githubusercontent.com", self.html)
        self.assertNotIn("DecompressionStream", self.html)


if __name__ == "__main__":
    unittest.main()
