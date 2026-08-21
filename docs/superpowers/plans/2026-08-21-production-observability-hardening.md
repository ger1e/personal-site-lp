# Production Observability and Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `personal-site-lp` reproducibly deployable, privacy-hardened, Sentry-observable, regression-tested, and truthfully verifiable in production.

**Architecture:** Preserve the static frontend and two Vercel Node error handlers. Browser Sentry remains loader-based with strict EU ingest allowlisting; Node Sentry remains centralized in `instrument.js`; CI and repository QA enforce the contract.

**Tech Stack:** Static HTML/CSS/JavaScript, Vercel Functions, Node.js 20+, `@sentry/node`, Python 3.12 unittest QA, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-21-production-observability-hardening-design.md`

## Global Constraints

- No frontend framework migration.
- No Sentry profiling dependency for current error handlers.
- Production trace sampling is 10%.
- Session Replay is disabled.
- Default PII, user information, cookies, request headers, and HTTP bodies are not sent to Sentry.
- Only exact required Sentry CDN/ingest origins are added to CSP.
- `personal-site-lp` is the canonical repository and Vercel project.
- Do not claim deployment success without a READY canonical Vercel deployment and route verification.

---

### Task 1: Dependency reproducibility

**Files:** `package.json`, `package-lock.json`, `.github/workflows/qa.yml`, `tests/test_qa.py`, `scripts/qa.py`

- [ ] Add a failing QA assertion that `package-lock.json` exists, uses lockfile v3, and pins the exact `@sentry/node` version declared in `package.json`.
- [ ] Verify the PR check fails before the lockfile exists.
- [ ] Generate and commit the lockfile, switch CI to `npm ci --ignore-scripts --no-audit --no-fund`, and rerun checks.

### Task 2: Sentry privacy and runtime contract

**Files:** `instrument.js`, `index.html`, `tests/test_qa.py`, `scripts/qa.py`

- [ ] Add failing checks for 10% production tracing, Replay disabled, `sendDefaultPii: false`, server `userInfo: false`, empty `httpBodies`, release tagging, and exact EU ingest allowlisting.
- [ ] Make only the minimum configuration changes required to satisfy the contract.
- [ ] Rerun tests and structural QA.

### Task 3: Serverless handler error-path verification

**Files:** `.github/workflows/qa.yml`, `tests/test_qa.py`

- [ ] Add assertions for 403/404 status codes, noindex header, HTML content type, cache-control, and non-empty body.
- [ ] Update the CI Node smoke script to assert the complete response contract.
- [ ] Rerun the smoke test and Python suite.

### Task 4: CSP and repository security regression gates

**Files:** `scripts/qa.py`, `tests/test_qa.py`

- [ ] Add fixtures for missing Sentry ingest allowlisting and forbidden wildcard script/network origins.
- [ ] Add a narrow secret-pattern audit that rejects Sentry auth tokens and PEM private-key headers while permitting the public Sentry DSN.
- [ ] Rerun the suite and structural audit.

### Task 5: Documentation truthfulness and deployment state

**Files:** `README.md`, `SECURITY.md`

- [ ] Explicitly mark `personal-site-lp` canonical and `git-landing-page` legacy/noncanonical.
- [ ] Document public DSN versus secret auth-token handling.
- [ ] Document exact verification commands and platform checks.

### Task 6: Final verification and production handoff

- [ ] Verify final branch/PR checks.
- [ ] Inspect Vercel `personal-site-lp` deployment state.
- [ ] If READY, verify `/`, `/403`, `/404`, headers, and runtime errors/logs.
- [ ] If not deployed, do not deploy the legacy project; report the exact missing Git-link/domain action.
