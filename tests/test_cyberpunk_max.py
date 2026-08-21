from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"
CSS = ROOT / "site.css"
JS = ROOT / "site.js"
PORTRAIT_FIX = ROOT / "portrait-fix.js"
PORTRAIT_CHUNKS = [ROOT / "portrait" / f"{i}.b64" for i in range(6)]

class CanonicalBlueSiteContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.css = CSS.read_text(encoding="utf-8")
        cls.js = JS.read_text(encoding="utf-8")
        cls.portrait_fix = PORTRAIT_FIX.read_text(encoding="utf-8")
        cls.all = "\n".join((cls.html, cls.css, cls.js, cls.portrait_fix))

    def test_identity_and_visual_contract(self):
        for token in ("GERGŐ ILLY","CYBERSECURITY PROFESSIONAL","Cybersecurity Consultant / Cyber Threat Hunter","Budapest, Hungary","visitor@gergoilly.hu: ~ — zsh"):
            self.assertIn(token, self.all)
        for color in ("#0f62fe","#78a9ff","#02060d"):
            self.assertIn(color, self.all.lower())
        self.assertNotIn("CIGANY.EXE", self.all)
        self.assertNotIn("rotund-operator", self.all)
        self.assertNotIn("spotify", self.all.lower())

    def test_canonical_boot_and_modules(self):
        for token in ("connecting to gergoilly.hu...","handshake complete","PTY allocated","cat /etc/motd.d/pepe","init landing_page --navigator","loading ${m.padEnd(18)}","navigator initialized","status ready","⣿⣿⣿⣿⣿⣿"):
            self.assertIn(token, self.all)

    def test_ibm_header_and_single_activity_led(self):
        self.assertIn("icons/ibm.svg", self.html)
        self.assertIn('id="status-led"', self.html)
        self.assertIn(".status-led", self.css)
        for token in ("PWR", "NET LED", "TTY LED", "IO LED", "hardware-led", "led-bank"):
            self.assertNotIn(token, self.all)

    def test_portrait_and_links(self):
        self.assertIn('src="data:image/gif;base64,', self.html)
        self.assertIn('src="/portrait-fix.js"', self.html)
        self.assertTrue(all(p.exists() for p in PORTRAIT_CHUNKS))
        total = sum(len(p.read_text(encoding="utf-8").strip()) for p in PORTRAIT_CHUNKS)
        self.assertGreater(total, 25_000)
        self.assertIn("data:image/webp;base64,", self.portrait_fix)
        self.assertIn("Array.from({length:6}", self.portrait_fix)
        self.assertIn('href="mailto:mail@gergoilly.hu"', self.html)
        self.assertIn('aria-label="Email Gergő Illy"', self.html)
        self.assertIn('href="https://linkedin.com/in/gergoilly"', self.html)

    def test_terminal_rain_and_input_behavior(self):
        for token in ('id="matrix-bg"','id="matrix-fg"',"Europe/Budapest","grid-template-rows:30px minmax(0,1fr) auto","overscroll-behavior:contain","history","ArrowUp","ArrowDown","Tab","speed:13.5","speed:23.5"):
            self.assertIn(token, self.all)
        self.assertNotIn("matrix [normal|dense|off]", self.all)
        self.assertNotIn("base==='matrix'", self.all)

    def test_glitch_max_controller(self):
        for token in ("micro-raster","command-shear","sync-fault","hard-fault","catastrophic()","hard()","schedule(catastrophic","schedule(hard","fault-layer","portraitGlitch","wordSlice","phosphorHit"):
            self.assertIn(token, self.all)

    def test_procedural_sound_controls(self):
        for token in ("AudioContext","sound on","sound off","sound test","sound status","audio.unlock","createOscillator","createBufferSource","ctx.resume"):
            self.assertIn(token, self.all)
        self.assertNotIn("<audio", self.all.lower())
        self.assertNotIn(".mp3", self.all.lower())
        self.assertNotIn(".wav", self.all.lower())

    def test_accessibility_and_mobile(self):
        for token in (":focus-visible","prefers-reduced-motion:reduce","@media(pointer:coarse)","@media(max-width:800px)","calc(61.8svh - 26px)","height:36svh"):
            self.assertIn(token, self.all)

if __name__ == "__main__":
    unittest.main()
