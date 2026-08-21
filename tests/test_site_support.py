import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SiteSupportTests(unittest.TestCase):
    def test_manifest_and_vercel_json_parse(self):
        json.loads((ROOT/'site.webmanifest').read_text()); json.loads((ROOT/'vercel.json').read_text())
    def test_required_public_support_files_exist(self):
        for name in ['favicon.svg','robots.txt','sitemap.xml','404.html','assets/social-card.png']: self.assertTrue((ROOT/name).is_file(),name)
    def test_robots_points_to_canonical_sitemap(self): self.assertIn('https://gergoilly.hu/sitemap.xml',(ROOT/'robots.txt').read_text())
if __name__=='__main__':unittest.main()
