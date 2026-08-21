from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
DSN_HOST = "o4511932881502208.ingest.de.sentry.io"
LOADER_HOST = "js.sentry-cdn.com"
BUNDLE_HOST = "browser.sentry-cdn.com"


class SentryIntegrationTests(unittest.TestCase):
    def test_node_sdk_is_pinned(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertEqual(package["dependencies"]["@sentry/node"], "10.70.0")
        self.assertNotIn("@sentry/profiling-node", package["dependencies"])

    def test_node_instrumentation_is_privacy_hardened(self):
        text = (ROOT / "instrument.js").read_text(encoding="utf-8")
        self.assertIn("sendDefaultPii: false", text)
        self.assertIn("userInfo: false", text)
        self.assertIn("httpBodies: []", text)
        self.assertIn("0.1", text)
        self.assertIn("VERCEL_GIT_COMMIT_SHA", text)

    def test_ci_can_disable_sentry_delivery(self):
        instrument = (ROOT / "instrument.js").read_text(encoding="utf-8")
        workflow = (ROOT / ".github" / "workflows" / "qa.yml").read_text(encoding="utf-8")
        self.assertIn('enabled: process.env.SENTRY_ENABLED !== "false"', instrument)
        self.assertIn("SENTRY_ENABLED: 'false'", workflow)

    def test_ci_matches_vercel_node_major(self):
        workflow = (ROOT / ".github" / "workflows" / "qa.yml").read_text(encoding="utf-8")
        self.assertIn("node-version: '24'", workflow)

    def test_error_routes_load_sentry_first(self):
        for code in (403, 404):
            text = (ROOT / "api" / f"{code}.js").read_text(encoding="utf-8")
            self.assertTrue(text.startswith('const Sentry=require("../instrument.js");'))
            self.assertIn("Sentry.captureException(error)", text)
            self.assertIn("Sentry.flush(1500)", text)

    def test_browser_loader_and_privacy_defaults(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn(f"https://{LOADER_HOST}/", text)
        self.assertIn("window.sentryOnLoad", text)
        self.assertIn("sendDefaultPii:false", text)
        self.assertIn("replaysSessionSampleRate:0", text)
        self.assertIn("replaysOnErrorSampleRate:0", text)
        self.assertIn("delete event.request.headers", text)

    def test_both_csps_allow_only_required_sentry_hosts(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        vercel = (ROOT / "vercel.json").read_text(encoding="utf-8")
        for text in (index, vercel):
            self.assertIn(LOADER_HOST, text)
            self.assertIn(BUNDLE_HOST, text)
            self.assertIn(DSN_HOST, text)
        self.assertNotIn("*.sentry.io", vercel)
        self.assertNotIn("*.ingest.de.sentry.io", vercel)


if __name__ == "__main__":
    unittest.main()
