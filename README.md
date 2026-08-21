# personal-site-lp

Canonical source for **https://gergoilly.hu/** — a static personal landing page for threat hunting, cyber threat intelligence, and detection engineering.

## Production surface

- Static `index.html` frontend with two small Vercel Node serverless routes for truthful HTTP 403/404 responses.
- Rotund cyber-operator cat as the primary visual hero.
- Canonical URL, Open Graph/Twitter metadata, JSON-LD profile metadata, sitemap and `robots.txt`.
- Full favicon/PWA asset set and branded social preview.
- Restrictive CSP/security headers, keyboard focus styles, and reduced-motion support.
- Sentry browser error monitoring plus Node error/tracing instrumentation for the serverless routes.
- Production tracing is sampled at 10%; Session Replay and default PII collection are disabled.

## Runtime dependencies

The static frontend has no framework or build step. `@sentry/node` is pinned in `package.json` for the Vercel serverless functions. Node profiling is intentionally not installed because the only backend code is the lightweight 403/404 handlers.

## Local preview

```bash
npm install
python -m http.server 8080
```

The Python server previews the static page only. Vercel is required to exercise `/api/403` and `/api/404` as deployed serverless functions.

## QA

```bash
npm install --ignore-scripts --no-audit --no-fund
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/qa.py
```

GitHub Actions additionally executes both serverless handlers with the installed Sentry SDK as a runtime smoke test. Structural QA is invariant-based rather than byte-hash based.

## Sentry

`instrument.js` is loaded first by each Node handler. It records the Vercel environment and Git commit SHA as release metadata when available, enables structured logs, samples production traces at 10%, and disables default PII, user information, and HTTP-body collection.

The browser loader is restricted by CSP to Sentry's loader/bundle hosts and this project's exact EU ingest host. Browser Session Replay is disabled and request headers, cookies, and request bodies are removed before events are sent.

The DSN embedded in the frontend is a public client identifier. Administrative Sentry auth tokens, Vercel tokens, and other secrets must never be committed.

## Deployment

Vercel should deploy the repository root from `main`. No build command is required; Vercel installs the Node dependency for the serverless functions. Git-repository linkage and DNS/domain attachment are account/platform settings rather than repository code.

## Security

See [`SECURITY.md`](SECURITY.md). Do not commit `.env`, `.vercel`, credentials, auth tokens, or local dependency state.

## Links

- Website: https://gergoilly.hu/
- GitHub profile: https://github.com/ger1e
- Experimental/history repo: https://github.com/ger1e/landing-pages
