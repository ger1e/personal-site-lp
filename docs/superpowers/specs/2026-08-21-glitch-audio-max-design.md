<!-- GER1E-DOC-SCHEMA: v1 -->
<a id="glitch-audio-max-design"></a>
<div align="center">

<strong>Glitch + Audio MAX Design</strong><br/>
<sub>GER1E // PERSONAL SITE LP // DOCUMENTATION</sub>

</div>

<a id="goal"></a>
<sub><strong>01 // Goal</strong></sub>
Restore the blue IBM Carbon/Cobalt personal site and make it feel continuously alive through coordinated visual instability and procedural sound, without adding hardware LEDs, user-facing Matrix modes, RGB/VHS effects, or generic cyberpunk HUD clutter.

<a id="baseline"></a>
<sub><strong>02 // Baseline</strong></sub>
The Drive canonical spec remains authoritative for layout, palette, portrait, terminal, typography, clock, code rain, and accessibility. Code rain is permanent infrastructure, not a configurable mode.

<a id="motion-model"></a>
<sub><strong>03 // Motion model</strong></sub>
Three intensity layers share one event controller:

1. Ambient: permanent low-level motion including dual-layer icy-cobalt rain, wordmark breathing, cursor blink, tiny scan/raster phase drift, subtle terminal surface movement, and occasional micro-slice glitches.
2. Reactive: typing, Enter, command success/error, terminal output, link interactions, and boot events emit coordinated visual and audio cues.
3. Catastrophic: rare 150–500 ms full-frame sync faults with scan compression, framebuffer displacement, blackout strips, localized terminal/portrait/wordmark desynchronization, then an immediate clean recovery. Rare hard faults may briefly freeze/offset multiple layers before re-lock.

A glitch governor prevents heavy effects from overlapping, guarantees recovery, and suppresses violent motion under `prefers-reduced-motion`.

<a id="glitch-vocabulary"></a>
<sub><strong>04 // Glitch vocabulary</strong></sub>
- micro horizontal raster skips and 1–2 px line offsets
- terminal phosphor pulse and short framebuffer shear
- wordmark multi-slice clipping/displacement
- portrait horizontal slice tear while preserving facial geometry
- scanline compression and partial blackout strips
- code-rain acceleration spikes during activity/faults
- short full-frame horizontal roll / sync-loss events
- clustered glitch bursts rather than metronomic timing

No rainbow RGB split, blur-heavy VHS filter, face warping, or permanent unreadable distortion.

<a id="audio-model"></a>
<sub><strong>05 // Audio model</strong></sub>
Use Web Audio API only; no external audio assets. Audio unlocks on first user gesture and remains user-controllable through terminal commands.

Cues:
- randomized mechanical key tick
- Enter thunk
- backspace click
- Tab/autocomplete chirp
- command success chirp
- command error rasp/fault burst
- boot handshake/relay sequence
- link interaction click
- micro/medium/catastrophic glitch tears
- low machine-room ambience bed after audio unlock

Terminal controls: `sound on`, `sound off`, `sound <0-100>`, `sound test`.

<a id="interaction-architecture"></a>
<sub><strong>06 // Interaction architecture</strong></sub>
Use one `EventTarget`-based event bus. Producers emit semantic events such as `type`, `backspace`, `execute`, `success`, `error`, `output`, `link`, `boot`, `glitch:micro`, `glitch:medium`, `glitch:catastrophic`, and `glitch:hard`. Visual and audio consumers subscribe independently.

<a id="user-facing-command-changes"></a>
<sub><strong>07 // User-facing command changes</strong></sub>
Remove all `matrix` commands and related state. Permanent rain remains enabled. Add only the `sound` command family.

<a id="accessibility-and-safety"></a>
<sub><strong>08 // Accessibility and safety</strong></sub>
- `prefers-reduced-motion` disables autonomous heavy glitches and motion-intensive transforms while preserving static styling and terminal function.
- Sound never plays before browser gesture unlock.
- No hidden tracking is added; existing Sentry privacy configuration stays intact.
- Site remains keyboard/touch usable throughout effects.

<a id="verification"></a>
<sub><strong>09 // Verification</strong></sub>
Regression tests must assert: no Matrix command surface, sound controls exist, Web Audio is procedural, shared event bus exists, catastrophic/hard fault scheduling exists, no hardware LED UI is introduced, reduced-motion support remains, and Sentry/CSP/security tests still pass.

<p align="center"><sub>GER1E // PERSONAL SITE LP // MOBILE-SAFE DOCUMENTATION</sub></p>
