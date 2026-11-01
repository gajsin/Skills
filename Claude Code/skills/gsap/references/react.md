# React and Next.js

Read for GSAP work in React. Create animations and measure DOM only in the
client lifecycle. In Next.js App Router, put `"use client"` at the appropriate
client boundary; do not turn unrelated server components into client components.

## Choose the existing integration

Use `useGSAP()` from `@gsap/react` when available; it is preferred for a new
integration. Keep a correct existing `gsap.context()` implementation. Add only
missing packages required by the chosen setup, using the project's package manager.

`useGSAP()` scopes selectors and automatically reverts GSAP objects created during
its setup. Attach the scope ref to the actual component root. Direct element refs
are also valid targets; unscoped selectors can affect other component instances.

```jsx
"use client";

import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);

export function AnimatedSection({ endX = 100 }) {
  const root = useRef(null);
  const { contextSafe } = useGSAP(() => {
    gsap.to(".box", { x: endX });
  }, {
    scope: root,
    dependencies: [endX],
    revertOnUpdate: true
  });

  const onClick = contextSafe(() => {
    gsap.to(".box", { rotation: "+=90", overwrite: "auto" });
  });

  return (
    <section ref={root}>
      <button className="box" onClick={onClick}>Animate</button>
    </section>
  );
}
```

The hook defaults to an empty dependency list, so ordinary renders do not repeat
setup. Declare changing inputs that should rebuild the animation. With
`revertOnUpdate: true`, the old context is reverted before each dependency-driven
rebuild; otherwise its objects remain tracked until context teardown.

## Objects created after setup

With `useGSAP`, wrap callbacks that create GSAP objects later in `contextSafe()`:
event handlers, delayed callbacks, and similar entry points. With an existing
`gsap.context()` integration, register that work through `context.add()` or
`self.add()` in its setup; do not add `@gsap/react` just for `contextSafe`.
Both approaches track the created GSAP objects in the owning context. Neither
removes native event listeners or cancels timers; return that cleanup from the
owning setup separately. React-managed
event props, such as the example's `onClick`, retain React's normal lifecycle.

## Existing effect-based setup

When using an effect instead of `useGSAP`, scope a `gsap.context()` and return
`context.revert()`. Revert restores the context's inline styles and disposes its
GSAP animations and ScrollTriggers. An isolated instance may also be explicitly
disposed by its owner; do not globally kill unrelated animations on unmount.

```jsx
import { useEffect, useRef } from "react";
import gsap from "gsap";

export function ExistingSection() {
  const root = useRef(null);

  useEffect(() => {
    const context = gsap.context(() => {
      gsap.to(".box", { x: 100 });
    }, root);
    return () => context.revert();
  }, []);

  return <section ref={root}><div className="box">Content</div></section>;
}
```

Keep setup and cleanup symmetric across dependency changes and development
Strict Mode's extra setup/cleanup cycle. A run-once flag does not repair a leak.

For scroll behavior, also read [scrolltrigger.md](scrolltrigger.md). See the
official [React guide](https://gsap.com/resources/React/) for advanced patterns.
