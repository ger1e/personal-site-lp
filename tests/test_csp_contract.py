import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ContentSecurityPolicyContractTests(unittest.TestCase):
    def test_page_csp_matches_canonical_vercel_response_header(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        vercel = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))

        match = re.search(
            r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
            index,
            re.IGNORECASE,
        )
        self.assertIsNotNone(match, "index.html must carry the static-host fallback CSP")

        header_values = [
            route["headers"]["Content-Security-Policy"]
            for route in vercel.get("routes", [])
            if isinstance(route, dict)
            and isinstance(route.get("headers"), dict)
            and isinstance(route["headers"].get("Content-Security-Policy"), str)
        ]
        self.assertEqual(len(header_values), 1, "vercel.json must define one canonical CSP header")
        self.assertEqual(
            match.group(1),
            header_values[0],
            "index.html CSP must mirror the canonical Vercel response-header CSP exactly",
        )


if __name__ == "__main__":
    unittest.main()
