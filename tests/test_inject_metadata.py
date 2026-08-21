import unittest
from scripts.inject_metadata import transform
HTML='<!doctype html><html><head><title>x</title><style>.cat-card{width:1px}</style></head><body></body></html>'
class InjectMetadataTests(unittest.TestCase):
    def test_adds_social_and_canonical_metadata(self):
        out=transform(HTML)
        for token in ['property="og:image"','name="twitter:image"','rel="canonical"','rel="icon"','rel="manifest"']: self.assertIn(token,out)
    def test_adds_cat_hero_override(self):
        out=transform(HTML); self.assertIn('pimp-cat-hero:start',out); self.assertIn('width:min(460px,38vw)',out)
    def test_is_idempotent(self):
        once=transform(HTML); self.assertEqual(once,transform(once))
if __name__=='__main__':unittest.main()
