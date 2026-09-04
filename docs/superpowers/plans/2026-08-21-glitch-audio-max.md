<!-- GER1E-DOC-SCHEMA: v1 -->
<a id="glitch-audio-max-implementation-plan"></a>
<div align="center">

<strong>Glitch + Audio MAX Implementation Plan</strong><br/>
<sub>GER1E // PERSONAL SITE LP // DOCUMENTATION</sub>

</div>

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add coordinated glitch-max visual behavior and procedural interaction audio to the restored blue personal site while removing user-facing Matrix controls.

**Architecture:** Keep the static single-page architecture. Add one shared semantic event bus inside `index.html`; visual and Web Audio consumers subscribe to the same events. Permanent code rain remains independent infrastructure but accepts short activity boosts from the FX controller.

**Tech Stack:** HTML5, CSS animations, vanilla JavaScript, Web Audio API, Python unittest contract tests, GitHub Actions, Vercel.

**Spec:** `docs/superpowers/specs/2026-08-21-glitch-audio-max-design.md`

<a id="global-constraints"></a>
<sub><strong>01 // Global Constraints</strong></sub>

- IBM Carbon/Cobalt baseline remains the visual source of truth.
- No hardware LEDs.
- No user-facing Matrix mode or Matrix commands.
- No RGB/rainbow glitch or VHS blur treatment.
- Sound must require a browser user gesture before playback.
- `prefers-reduced-motion` must suppress autonomous heavy motion.
- Preserve Sentry privacy and existing CSP/security behavior.

---

<a id="task-1-regression-contract"></a>
<sub><strong>02 // Task 1: Regression contract</strong></sub>

**Files:**
- Modify: `tests/test_cyberpunk_max.py`
- Test: `tests/test_cyberpunk_max.py`

**Interfaces:**
- Consumes: current restored `index.html`
- Produces: contract assertions for the new event/audio/glitch behavior

- [ ] Add failing assertions that `matrix [normal|dense|off]` and `base==='matrix'` are absent.
- [ ] Add failing assertions for `new EventTarget()`, `AudioContext`, `sound on`, `sound off`, `sound test`, `scheduleCatastrophic`, `scheduleHardFault`, `glitch:catastrophic`, and `glitch:hard`.
- [ ] Assert no hardware LED labels/components are introduced.
- [ ] Run `python -m unittest discover -s tests -v` and confirm the new assertions fail for missing functionality.

<a id="task-2-shared-fx-controller-and-permanent-rain"></a>
<sub><strong>03 // Task 2: Shared FX controller and permanent rain</strong></sub>

**Files:**
- Modify: `index.html`
- Test: `tests/test_cyberpunk_max.py`

**Interfaces:**
- Produces: `bus`, `emit(name, detail)`, semantic event listeners, permanent dense rain with activity boosts

- [ ] Remove `state.matrix`, Matrix command parsing, Matrix autocomplete, and `applyMatrix()`.
- [ ] Keep both rain canvases permanently active at the canonical dense baseline.
- [ ] Add shared `EventTarget` bus and `emit()` helper.
- [ ] Emit `output`, `type`, `backspace`, `execute`, `success`, `error`, `link`, and `boot` from existing interaction paths.
- [ ] Run unit tests and confirm Matrix-removal/event-bus assertions pass.

<a id="task-3-visual-glitch-stack"></a>
<sub><strong>04 // Task 3: Visual glitch stack</strong></sub>

**Files:**
- Modify: `index.html`
- Test: `tests/test_cyberpunk_max.py`

**Interfaces:**
- Consumes: semantic FX bus
- Produces: micro, reactive, medium, catastrophic, and hard-fault visual handlers

- [ ] Add CSS keyframes/classes for micro raster skip, terminal phosphor hit, command shear, error fault, scan compression, blackout strips, full-frame sync loss, and hard-fault recovery.
- [ ] Add one non-interactive fault overlay layer to the workstation.
- [ ] Implement a heavy-glitch governor using a lock timestamp so catastrophic/hard effects never overlap.
- [ ] Implement `scheduleMicro()`, `scheduleMedium()`, `scheduleCatastrophic()`, and `scheduleHardFault()` with randomized clustered timing.
- [ ] Bind typing/execute/success/error/link events to appropriately scaled visual effects.
- [ ] Preserve existing portrait and wordmark slice effects but route autonomous triggering through the governor.
- [ ] Disable autonomous heavy effects under reduced motion.
- [ ] Run unit tests.

<a id="task-4-procedural-web-audio-cues"></a>
<sub><strong>05 // Task 4: Procedural Web Audio cues</strong></sub>

**Files:**
- Modify: `index.html`
- Test: `tests/test_cyberpunk_max.py`

**Interfaces:**
- Consumes: semantic FX bus
- Produces: `audio` controller with `unlock`, `setEnabled`, `setVolume`, cue synthesis, and ambience

- [ ] Add lazy `AudioContext` creation on first pointer or keyboard gesture.
- [ ] Implement oscillator/noise primitives with short gain envelopes; do not load external media.
- [ ] Add cues for type, backspace, execute, success, error, link, boot, micro/medium/catastrophic/hard glitches.
- [ ] Add a subtle low machine ambience bed after unlock; stop it when sound is disabled.
- [ ] Add terminal handling for `sound on`, `sound off`, `sound <0-100>`, and `sound test`.
- [ ] Add sound command autocomplete/help text.
- [ ] Run unit tests.

<a id="task-5-full-regression-and-preview-verification"></a>
<sub><strong>06 // Task 5: Full regression and preview verification</strong></sub>

**Files:**
- Verify: `index.html`, `vercel.json`, `tests/*`, `.github/workflows/*`

**Interfaces:**
- Consumes: completed recovery branch
- Produces: merge-ready PR #5

- [ ] Run GitHub Actions QA on the exact PR head.
- [ ] Confirm Sentry/CSP/security tests still pass.
- [ ] Inspect PR preview or deployment response for successful 200 render and absence of runtime errors.
- [ ] Verify `/403` and `/404` remain genuine status routes.
- [ ] Review final diff for accidental Matrix controls, hardware LEDs, RGB/VHS effects, external audio assets, or unrelated refactors.

<p align="center"><sub>GER1E // PERSONAL SITE LP // MOBILE-SAFE DOCUMENTATION</sub></p>
