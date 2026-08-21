# Production Observability and Hardening Design

## Scope

Keep `personal-site-lp` a static-first Vercel site. Improve deployment correctness, Sentry observability, privacy controls, dependency reproducibility, CI regression coverage, error-route reliability, and operator documentation without introducing a frontend framework or unnecessary backend surface.

## Architecture

The browser remains a static `index.html` with the Sentry browser loader. Browser telemetry sends only to the project's explicit EU ingest host, disables Session Replay, disables default PII, and strips request cookies, headers, and bodies before events leave the page.

The only Node runtime remains the Vercel serverless error handlers. `instrument.js` initializes `@sentry/node` before handler code, tags Vercel environment and Git commit release metadata, enables logs, samples production traces at 10%, and disables user-info and HTTP-body collection. Profiling remains disabled because the handlers are tiny and profiling adds dependency/native-runtime cost without useful signal.

`vercel.json` is the authoritative HTTP security-header policy. The page-level CSP must never be broader than the server header. Sentry is allowlisted by exact CDN/ingest origins, Spotify remains the only other third-party surface, and frame embedding remains denied.

## Reliability and Supply Chain

Pin runtime dependencies exactly and commit an npm lockfile. CI uses `npm ci` rather than `npm install`, executes both serverless handlers with Sentry network delivery disabled, runs Python unit tests, and runs the repository structural audit. QA explicitly checks Sentry files, dependency pinning, CSP allowlists, privacy flags, and absence of committed secrets.

## Deployment

`ger1e/personal-site-lp` is the canonical source repository. The intended Vercel project is `personal-site-lp`. The older `git-landing-page` / `landing-pages` deployment is not considered canonical. Repository changes must not claim production success unless Vercel shows a READY deployment for the canonical project and the live routes are verified.

## Verification

A complete pass requires: repository tests green, reproducible npm dependency install, 403/404 handler smoke tests, security-policy checks, and—when the Vercel project is actually connected—production checks for `/`, `/403`, `/404`, CSP headers, and Sentry telemetry delivery. A missing Vercel Git connection is reported as a platform blocker rather than silently deploying the wrong project.
