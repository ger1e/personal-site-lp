# Security Policy

## Scope

This repository contains a static personal website plus two minimal Vercel Node serverless error routes. Security reports should concern code or configuration maintained in this repository, including the page, serverless handlers, Sentry instrumentation, Content Security Policy, repository automation, or a demonstrable vulnerability introduced by repository-controlled content.

Third-party sites and services linked by the page are outside this repository's security boundary and should be reported to their respective operators.

## Reporting a vulnerability

Please do not publish secrets, exploit details, or a working proof of concept in a public issue.

If GitHub exposes **Report a vulnerability** / private vulnerability reporting for this repository, use that channel. Otherwise, contact the repository owner through a private contact method listed on the GitHub profile and include:

- the affected file or behavior;
- reproducible steps;
- security impact;
- browser/platform details when relevant; and
- the minimum proof needed to validate the issue.

Reports that only describe cosmetic behavior, expected client-side source visibility, or vulnerabilities belonging solely to third-party services are not repository vulnerabilities.

## Telemetry and privacy

Sentry is configured for error monitoring and sampled tracing. Session Replay is disabled. Default PII collection, user information, HTTP request bodies, browser request headers, and browser cookies are excluded from telemetry by repository configuration.

The Sentry DSN/client key embedded in frontend code is intentionally public and is not an administrative credential. It grants event-ingestion capability only and must not be confused with a Sentry auth token.

## Secrets

No production secret, administrative API token, Vercel token, credential, private key, or private configuration value should ever be committed to this repository or embedded in `index.html`. Local `.env` and `.vercel` state are ignored by Git.
