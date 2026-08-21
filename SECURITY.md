# Security Policy

## Scope

This repository contains a static-first personal website plus two minimal Vercel Node serverless error routes. Security reports should concern code or configuration maintained here, including the page, serverless handlers, Sentry instrumentation, Content Security Policy, dependency lock, repository automation, or a demonstrable vulnerability introduced by repository-controlled content.

Third-party sites and services linked by the page are outside this repository's security boundary and should be reported to their respective operators.

## Reporting a vulnerability

Do not publish secrets, exploit details, or a working proof of concept in a public issue.

If GitHub exposes **Report a vulnerability** / private vulnerability reporting for this repository, use that channel. Otherwise, contact the repository owner through a private contact method listed on the GitHub profile and include the affected file or behavior, reproducible steps, security impact, relevant browser/platform details, and the minimum proof needed to validate the issue.

Reports describing only cosmetic behavior, expected client-side source visibility, or vulnerabilities belonging solely to third-party services are not repository vulnerabilities.

## Telemetry and privacy

Sentry is configured for error monitoring and sampled tracing. Production tracing is 10%. Session Replay is disabled. Default PII collection, user information, HTTP request bodies, browser request headers, and browser cookies are excluded by repository configuration.

CI sets `SENTRY_ENABLED=false`; automated tests exercise the instrumentation and serverless handlers without emitting telemetry.

The Sentry DSN/client key embedded in frontend/runtime code is intentionally public and is not an administrative credential. It permits client event ingestion and must not be confused with a Sentry auth token. Sentry administrative auth tokens remain secret and must be stored only in an approved secret store/environment when required for administrative operations such as release/source-map upload.

## Supply chain and CI controls

`@sentry/node` is pinned to an exact version and the full npm dependency graph is committed in `package-lock.json`. CI performs a clean `npm ci` on the same Node major used by Vercel, executes both error handlers, runs the regression suite, and runs structural QA.

Repository QA rejects broad wildcard script/network CSP sources, missing Sentry allowlist origins, committed `.env` files, Sentry administrative auth-token patterns, PEM private-key material, dependency-lock/version drift, broken metadata/assets, and routing/security-policy regressions. The public Sentry DSN is explicitly not treated as a secret.

## Secrets

No production secret, administrative API token, Vercel token, credential, private key, or private configuration value should ever be committed to this repository or embedded in `index.html`. Local `.env`, `.vercel`, `node_modules`, logs, and coverage state are ignored by Git.
