import unittest

from scripts.promote_cat import END, START, transform

HTML = '<!doctype html><html><head><style>.cat-card{width:1px}</style></head><body></body></html>'


class PromoteCatTests(unittest.TestCase):
    def test_promotes_cat_to_large_responsive_hero(self):
        out = transform(HTML)
        self.assertIn(START, out)
        self.assertIn('width:min(470px,39vw)', out)
        self.assertIn('@media(max-width:620px)', out)

    def test_transform_is_idempotent(self):
        once = transform(HTML)
        twice = transform(once)
        self.assertEqual(once, twice)
        self.assertEqual(twice.count(START), 1)
        self.assertEqual(twice.count(END), 1)

    def test_missing_style_close_is_rejected(self):
        with self.assertRaises(ValueError):
            transform('<html><head></head></html>')


if __name__ == '__main__':
    unittest.main()
