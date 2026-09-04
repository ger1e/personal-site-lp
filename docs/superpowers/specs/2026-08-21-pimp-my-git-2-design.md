<!-- GER1E-DOC-SCHEMA: v1 -->
<a id="pimp-my-git-20-design"></a>
<div align="center">

<strong>Pimp My Git 2.0 — Design</strong><br/>
<sub>GER1E // PERSONAL SITE LP // DOCUMENTATION</sub>

</div>

Date: 2026-08-21
Owner: ger1e
Status: Approved in chat; written-spec review pending

<a id="goal"></a>
<sub><strong>01 // Goal</strong></sub>

Turn the current GitHub presence into a signal-first public portfolio for threat hunting, CTI, detection engineering, and selected personal projects, while preserving the existing cyberpunk identity without letting style overwhelm repository quality.

<a id="scope"></a>
<sub><strong>02 // Scope</strong></sub>

<a id="canonical-personal-site"></a>
<sub><strong>03 // Canonical personal site</strong></sub>

`ger1e/personal-site-lp` is the canonical public personal-site repository.

Planned changes:
- Replace the placeholder README with a substantive project README.
- Document purpose, architecture, local usage, deployment assumptions, accessibility/reduced-motion behavior, and security posture.
- Add `.editorconfig`, `.gitattributes`, `.gitignore`, and `SECURITY.md` where useful and non-duplicative.
- Add bounded GitHub Actions QA focused on meaningful invariants and smoke checks.
- Do not add dependency-management automation unless dependencies are introduced.

<a id="landing-pages-repository"></a>
<sub><strong>04 // Landing-pages repository</strong></sub>

`ger1e/landing-pages` becomes a playground/history repository rather than a competing canonical personal site.

Planned changes:
- Replace the placeholder README with a clear purpose statement.
- Point users to `ger1e/personal-site-lp` as the canonical site.
- Keep historical/experimental landing-page work intact unless it is clearly obsolete or broken.
- Avoid destructive cleanup unrelated to presentation or correctness.

<a id="cti-repository"></a>
<sub><strong>05 // CTI repository</strong></sub>

`ger1e/cti-enrichment-gateway` remains private and engineering-first.

Planned changes:
- No broad redesign in this pass.
- Preserve its existing stronger repository hygiene.
- Only make bounded presentation/hygiene changes if a concrete inconsistency is found during implementation.

<a id="github-profile"></a>
<sub><strong>06 // GitHub profile</strong></sub>

Target presentation:
- Threat Hunter / CTI / Detection Engineering first.
- Original work prioritized over forks and course repositories.
- Distinctive visual identity, but restrained enough to remain credible to technical reviewers and recruiters.
- Avoid badge walls, vanity counters, and generic skill-logo clutter.

A dedicated `ger1e/ger1e` profile README is desirable, but creating the special profile repository is outside the currently available GitHub connector capability. If the repository is created separately, this pass can populate it afterward.

<a id="public-portfolio-hierarchy"></a>
<sub><strong>07 // Public portfolio hierarchy</strong></sub>

Preferred visible order:
1. Canonical personal site / original public engineering work.
2. Original cybersecurity, automation, or research tooling that is safe to expose publicly.
3. Selected experiments or creative technical work.
4. Forks and training/course repositories only where they add clear signal.

The large `godot` fork and old bash-learning repository should not visually dominate the profile over original work. This design does not require deleting them.

<a id="readme-design"></a>
<sub><strong>08 // README design</strong></sub>

The canonical site README should be concise and technical, with these sections where applicable:
- Project identity and purpose.
- What the site demonstrates.
- Stack and implementation model.
- Local usage.
- Deployment model.
- Accessibility and reduced-motion behavior.
- Security and privacy notes.
- Repository structure.
- Canonical links.

No marketing filler, generic AI copy, or badge cemetery.

<a id="repository-hygiene"></a>
<sub><strong>09 // Repository hygiene</strong></sub>

For `personal-site-lp`, add only files that materially improve maintainability or safety:
- `.editorconfig`
- `.gitattributes`
- `.gitignore`
- `SECURITY.md`
- `.github/workflows/qa.yml`

Do not introduce frameworks, package managers, build systems, or dependencies solely to make the repository look more sophisticated.

<a id="qa-design"></a>
<sub><strong>10 // QA design</strong></sub>

The QA workflow must not reproduce the previous brittle content-hash check.

Checks should validate behavior or structural invariants instead of exact file bytes. Candidate checks:
- Required files exist.
- `index.html` is non-empty and contains a valid document skeleton.
- Required identity/navigation strings are present only where they represent intended functionality.
- No merge-conflict markers.
- No obvious accidental secret material or `.env` files committed.
- No broken local asset references where cheaply testable.
- Basic HTML parsing/sanity checks using tools available on the runner without creating a dependency-heavy stack.

A byte-for-byte SHA256 assertion is explicitly forbidden for routine QA because harmless edits should not break deployment.

<a id="security-posture"></a>
<sub><strong>11 // Security posture</strong></sub>

The site is static and should remain low-complexity.

Principles:
- Minimize third-party execution.
- Keep Content Security Policy restrictive.
- Avoid storing secrets in the repository or frontend.
- Preserve `rel="noopener noreferrer"` where appropriate for external targets.
- Avoid telemetry or analytics unless explicitly requested later.
- Prefer no dependency chain over an unnecessary frontend toolchain.

<a id="accessibility-and-ux"></a>
<sub><strong>12 // Accessibility and UX</strong></sub>

Preserve the visual identity while keeping:
- `prefers-reduced-motion` support.
- Keyboard-visible focus states.
- Responsive/mobile behavior.
- Readable semantic content despite visual effects.

Visual effects are not a reason to break navigation, resize behavior, or keyboard interaction.

<a id="non-goals"></a>
<sub><strong>13 // Non-goals</strong></sub>

This pass does not:
- Rebuild the personal site from scratch.
- Add a frontend framework.
- Create unnecessary npm dependencies.
- Delete large repositories or forks merely for aesthetics.
- Make the private CTI repository public.
- Add fake metrics, contribution generators, star farming, or other profile-gaming tricks.

<a id="implementation-strategy"></a>
<sub><strong>14 // Implementation strategy</strong></sub>

Use bounded, reviewable changes on the default branches. Prefer direct, minimal edits over repository-wide rewrites. Verify each changed repository after writes and run or inspect the new QA workflow when possible.

<a id="success-criteria"></a>
<sub><strong>15 // Success criteria</strong></sub>

The pass is complete when:
- `personal-site-lp` clearly reads as the canonical maintained personal site.
- `landing-pages` clearly reads as experimental/history rather than a competing canonical site.
- Repository docs and hygiene are materially improved without unnecessary tooling.
- QA protects meaningful invariants without brittle exact-content hashes.
- No destructive cleanup occurs outside the approved scope.
- The profile direction is documented for later `ger1e/ger1e` activation.

<p align="center"><sub>GER1E // PERSONAL SITE LP // MOBILE-SAFE DOCUMENTATION</sub></p>
