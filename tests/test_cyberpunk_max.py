from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"


class CanonicalBlueSiteContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_identity_and_visual_contract(self):
        for token in (
            "GERGŐ ILLY",
            "CYBERSECURITY PROFESSIONAL",
            "Cybersecurity Consultant / Cyber Threat Hunter",
            "Budapest, Hungary",
            "#0F62FE",
            "#78A9FF",
            "#02060D",
            "visitor@gergoilly.hu: ~ — zsh",
        ):
            self.assertIn(token, self.html)
        self.assertNotIn("CIGANY.EXE", self.html)
        self.assertNotIn("rotund-operator", self.html)
        self.assertNotIn("sound-link", self.html)
        self.assertNotIn("spotify", self.html.lower())

    def test_portrait_and_links(self):
        self.assertIn("1zgxo_yoYnLX6FGoh8CvR7uX9H62ZME5y", self.html)
        self.assertIn('href="mailto:mail@gergoilly.hu"', self.html)
        self.assertIn('aria-label="Email Gergő Illy"', self.html)
        self.assertIn('href="https://linkedin.com/in/gergoilly"', self.html)
        self.assertIn('target="_blank" rel="noopener noreferrer"', self.html)

    def test_terminal_rain_and_input_behavior(self):
        for token in (
            'id="matrix-bg"',
            'id="matrix-fg"',
            "Europe/Budapest",
            "grid-template-rows:30px minmax(0,1fr) auto",
            "overscroll-behavior:contain",
            "history",
            "ArrowUp",
            "ArrowDown",
            "Tab",
        ):
            self.assertIn(token, self.html)
        self.assertNotIn("matrix [normal|dense|off]", self.html)
        self.assertNotIn("base==='matrix'", self.html)
        self.assertNotIn("applyMatrix()", self.html)

    def test_glitch_max_controller(self):
        for token in (
            "new EventTarget()",
            "glitch:micro",
            "glitch:medium",
            "glitch:catastrophic",
            "glitch:hard",
            "scheduleCatastrophic",
            "scheduleHardFault",
            "fault-layer",
            "syncFault",
            "hardFault",
            "phosphorHit",
        ):
            self.assertIn(token, self.html)

    def test_procedural_sound_controls(self):
        for token in (
            "AudioContext",
            "sound on",
            "sound off",
            "sound test",
            "audio.unlock",
            "audio.setVolume",
            "createOscillator",
            "createBufferSource",
        ):
            self.assertIn(token, self.html)
        self.assertNotIn("<audio", self.html.lower())
        self.assertNotIn(".mp3", self.html.lower())
        self.assertNotIn(".wav", self.html.lower())

    def test_no_hardware_led_surface(self):
        for token in ("PWR", "NET LED", "TTY LED", "IO LED", "hardware-led", "led-bank"):
            self.assertNotIn(token, self.html)

    def test_accessibility_and_mobile(self):
        for token in (
            ":focus-visible",
            "prefers-reduced-motion:reduce",
            "@media(pointer:coarse)",
            "@media(max-width:800px)",
            "calc(61.8svh - 26px)",
            "height:36svh",
        ):
            self.assertIn(token, self.html)


if __name__ == "__main__":
    unittest.main()
