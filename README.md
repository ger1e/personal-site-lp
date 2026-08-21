# personal-site-lp

Canonical source for **https://gergoilly.hu/** — a static-first personal landing page for threat hunting, cyber threat intelligence, and detection engineering.

## Production surface

- Static `index.html` frontend; no frontend framework or build step.
- Two minimal Vercel Node serverless routes provide truthful HTTP 403/404 responses.
- Rotund cyber-operator cat as the primary visual hero.
- Canonical URL, Open Graph/Twitter metadata, JSON-LD profile metadata, sitemap, `robots.txt`, favicon/PWA assets, and branded social preview.
- Restrictive CSP/security headers, keyboard focus styles, coarse-pointer handling, and reduced-motion support.
- Browser Sentry error monitoring plus Node error/tracing instrumentation for the serverless routes.
- Production traces sampled at 10%; Session Replay and default PII collection disabled.

## Runtime and dependencies

Vercel currently runs the project on Node 24.x, and GitHub Actions tests the same Node major. `@sentry/node` is pinned exactly in `package.json`; the complete npm dependency graph is committed in `package-lock.json`. Node profiling is intentionally absent because the backend surface is only the lightweight 403/404 handlers.

Install reproducibly with:

```bash
npm ci --ignore-scripts --no-audit --no-fund
```

## Local preview

```bash
npm ci --ignore-scripts --no-audit --no-fund
python -m http.server 8080
```

The Python server previews the static page only. Vercel is required to exercise the serverless routing behavior exactly as deployed.

## QA

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/qa.py
```

GitHub Actions additionally performs a clean `npm ci`, executes both serverless handlers with Sentry network delivery disabled, validates status/body/cache/noindex behavior, then runs the full Python regression suite and structural audit.

The audit gates dependency-lock integrity, exact Sentry version pinning, browser/server privacy defaults, CSP allowlists, wildcard CSP regressions, committed `.env` files, Sentry administrative auth-token patterns, PEM private-key material, broken local assets, metadata, security.txt, and routing invariants.

## Sentry

`instrument.js` is loaded first by each Node handler. It records the Vercel environment and Git commit SHA as release metadata when available, enables structured logs, samples production traces at 10%, and disables default PII, user information, and HTTP-body collection. CI sets `SENTRY_ENABLED=false` so test runs never emit telemetry.

The browser loader is restricted by CSP to Sentry's loader/bundle hosts and this project's exact EU ingest host. Browser Session Replay is disabled; request headers, cookies, and request bodies are removed before events are sent.

The DSN embedded in frontend/runtime code is a public client identifier, not an administrative secret. Sentry auth tokens, Vercel tokens, credentials, private keys, `.env`, and `.vercel` state must never be committed.

## Deployment

`ger1e/personal-site-lp` and the Vercel project named `personal-site-lp` are canonical. The older `ger1e/landing-pages` / `git-landing-page` deployment is legacy/experimental and must not be used as proof that this repository is live.

Production is considered verified only when the canonical Vercel project shows a READY deployment from `main` and `/`, `/403`, and `/404` have been checked on that deployment. Git-repository linkage and domain attachment are Vercel account/platform settings rather than repository code.

## Security

See [`SECURITY.md`](SECURITY.md).

## Links

- Website: https://gergoilly.hu/
- GitHub profile: https://github.com/ger1e
- Legacy/experimental repo: https://github.com/ger1e/landing-pages
