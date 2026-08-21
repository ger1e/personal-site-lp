# personal-site-lp

Canonical source for **https://gergoilly.hu/** — a static personal landing page for threat hunting, cyber threat intelligence, and detection engineering.

## Production surface

- Single static `index.html`; no frontend framework, package manager, or application runtime.
- Rotund cyber-operator cat promoted to the primary visual hero while preserving the embedded image payload.
- Canonical URL, Open Graph/Twitter metadata, JSON-LD profile metadata, sitemap and `robots.txt`.
- Full favicon/PWA asset set and branded social preview.
- Branded HTTP 403/404 surfaces with truthful Vercel status handling.
- Restrictive CSP/security headers, keyboard focus styles, and reduced-motion support.

## Local preview

```bash
python -m http.server 8080
```

## QA

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/qa.py
```

Structural QA is invariant-based rather than byte-hash based. `scripts/promote_cat.py` manages the cat-hero override idempotently so the large embedded WebP never needs to be copied or re-encoded just to change layout.

## Deployment

Vercel deploys the repository root from `main`. No build command is required. DNS/domain attachment remains an account/platform setting rather than repository code.

## Security

No secrets belong in the frontend or repository. The public page requires no application backend or analytics layer. See [`SECURITY.md`](SECURITY.md).

## Links

- Website: https://gergoilly.hu/
- GitHub profile: https://github.com/ger1e
- Experimental/history repo: https://github.com/ger1e/landing-pages
