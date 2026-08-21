# personal-site-lp

Canonical personal landing page for `ger1e` — threat hunting, cyber threat intelligence, and detection engineering.

The site is intentionally small: one static HTML document, no frontend framework, no package manager, no build pipeline, and no application runtime. The visual layer is aggressive; the repository underneath it is deliberately boring.

## What this repository contains

- A responsive static landing page in `index.html`.
- Client-side visual effects and interactions implemented directly in HTML/CSS/JavaScript.
- A restrictive Content Security Policy defined in the document.
- Keyboard-visible focus styling and `prefers-reduced-motion` handling.
- Dependency-free structural QA implemented with the Python standard library.
- GitHub Actions CI for pull requests and changes to the maintained branch.

## Local preview

Any static HTTP server works. With Python 3:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080/`.

There is no install step and no build step.

## QA

Run the unit tests and repository audit locally:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/qa.py
```

The audit checks structural invariants rather than exact file bytes. It verifies the document skeleton, CSP presence, reduced-motion and keyboard-focus support, merge-conflict markers, accidental `.env` files, and repository-local asset references.

A harmless HTML edit should not require updating a magic SHA256 value.

## Deployment

Deploy the repository root as a static site. No server-side runtime or build command is required.

For a platform such as Vercel, the expected model is a direct static deployment of the repository root from `main`. Platform-specific configuration should only be added if the deployment actually needs it.

## Security and privacy

- No secrets belong in the frontend or repository.
- The page does not require an application backend.
- The CSP is intentionally restrictive.
- Third-party destinations and embeds remain outside this repository's trust boundary.
- No analytics or tracking layer is required by the project.

See [`SECURITY.md`](SECURITY.md) for vulnerability reporting guidance.

## Accessibility and failure tolerance

The visual effects are non-essential. The page keeps semantic content and navigation usable when animation is disabled, when a user requests reduced motion, and when navigating by keyboard.

Changes that make the effects prettier while breaking mobile sizing, focus states, or navigation are regressions.

## Repository structure

```text
.
├── .github/workflows/qa.yml   # CI
├── docs/superpowers/          # approved design and implementation plan
├── scripts/qa.py              # dependency-free repository audit
├── tests/test_qa.py           # audit regression tests
├── index.html                 # complete static site
├── README.md
└── SECURITY.md
```

## Canonical links

- GitHub profile: https://github.com/ger1e
- Canonical repository: https://github.com/ger1e/personal-site-lp
- Experimental/history repository: https://github.com/ger1e/landing-pages
