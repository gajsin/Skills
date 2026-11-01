---
name: gsap
description: "Implement GSAP website animations with React lifecycle or ScrollTrigger guidance when needed. Invoke explicitly with $gsap."
license: MIT
---

# GSAP

Implement the requested website animation in the existing project. Use this
skill only when explicitly requested and GSAP has been selected for the task.
Preserve the approved design and a suitable existing animation integration.

## Read only the relevant guidance

- **React or Next.js:** read [react.md](references/react.md) before changing
  lifecycle, targets, dependencies, or event handlers.
- **Scroll-driven behavior:** read [scrolltrigger.md](references/scrolltrigger.md)
  before changing triggers, scrub, pinning, or scroll-dependent geometry.
- **Scroll animation in React:** read both; use React's owning context to clean
  up the ScrollTriggers it creates.
- **Other GSAP work:** neither reference is mandatory unless its subject applies.

## Shared implementation rules

Inspect the affected code and installed packages first. Reuse the project's
integration and package manager; install only a missing dependency needed for
the agreed behavior. Invoking this skill does not require adding React,
`@gsap/react`, a smooth-scroll library, or replacing a suitable CSS animation.

Keep targets scoped to the feature or component. Clean up its animations,
triggers, listeners, and timers when their owner is disposed or rebuilt, without
destroying another feature's objects. Respect reduced-motion preferences and
keep essential content readable without animation. For responsive branches,
reuse the project's approach or `gsap.matchMedia()` when appropriate.

Verify the behavior affected by the change with existing project tools. Lifecycle
changes need cleanup/re-mount checks; scroll or layout changes need relevant
position and viewport checks. Choose checks for the remaining risk rather than
bootstrapping an unrelated environment or running every animation scenario.

For APIs beyond these references, consult the official [GSAP core](https://gsap.com/docs/v3/GSAP/)
and [timeline](https://gsap.com/docs/v3/GSAP/Timeline/) documentation as needed.
