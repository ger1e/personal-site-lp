# personal-site-lp

Canonical personal landing page for `ger1e` — threat hunting, cyber threat intelligence, and detection engineering.

Production domain: **https://gergoilly.hu/**

The site is intentionally small: one static HTML document, no frontend framework, no package manager, no application runtime. The visual layer is aggressive; the repository underneath it is deliberately boring.

## What this repository contains

- A responsive static landing page in `index.html` with the rotund cyber-operator cat as a primary hero element.
- Client-side visual effects and interactions implemented directly in HTML/CSS/JavaScript.
- Canonical/social metadata managed idempotently by `scripts/inject_metadata.py`.
- Branded social preview asset, favicon, web manifest, `robots.txt`, sitemap, and custom 404 page.
- Vercel security headers in `vercel.json`.
- A restrictive Content Security Policy defined in the document.
- Keyboard-visible focus styling and `prefers-reduced-motion` handling.
- Dependency-free structural QA implemented with the Python standard library.
- GitHub Actions CI for pull requests and changes to the maintained branch.

## Local preview

```bash
python -m http.server 8080
```

## QA

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/qa.py
```

The audit checks structural invariants rather than exact file bytes. `site-metadata.yml` runs the idempotent metadata injector against the real page before QA and commits managed metadata/hero changes on `main` only when necessary.

## Deployment

Vercel should deploy the repository root directly from `main`; no build command or server runtime is required. The canonical URL is `https://gergoilly.hu/`. DNS/domain attachment remains a Vercel account setting rather than repository code.

## Security and privacy

- No secrets belong in the frontend or repository.
- The page does not require an application backend.
- The CSP is intentionally restrictive.
- Third-party destinations and embeds remain outside this repository's trust boundary.
- No analytics or tracking layer is required by the project.
- Vercel response headers add `nosniff`, strict referrer policy, a restrictive Permissions Policy, and HSTS.

See [`SECURITY.md`](SECURITY.md) for vulnerability reporting guidance.

## Canonical links

- Website: https://gergoilly.hu/
- GitHub profile: https://github.com/ger1e
- Canonical repository: https://github.com/ger1e/personal-site-lp
- Experimental/history repository: https://github.com/ger1e/landing-pages
