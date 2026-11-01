# ScrollTrigger

Use for animation or state driven by scroll. Register the loaded plugin once
before use in the client lifecycle:

```js
gsap.registerPlugin(ScrollTrigger);
```

Import or load GSAP and ScrollTrigger through the project's existing setup.

## Trigger geometry and behavior

`start` and `end` strings use `"triggerPosition scrollerPosition"`, such as
`"top 80%"` or `"bottom center"`. The viewport is the default scroller; use
`scroller` only for an actual custom scroll container. `endTrigger` can supply a
different end element. Numeric values are absolute scroll positions; `"+=300"`
is a distance past start, `"+=100%"` uses the scroller's height, and `"max"` uses
its maximum scroll. `clamp(...)` keeps positions inside page bounds.

Choose the control model that matches the request:

- `scrub: true` ties progress directly to scrolling; a number gives a catch-up
  duration in seconds.
- `toggleActions` controls discrete entry/exit behavior, in order: enter, leave,
  enter back, leave back. For example, `"play reverse play reverse"`.

Do not configure `toggleActions` to control a scrubbed playhead: scrub owns its
progress. Callbacks such as `onEnter`, `onLeave`, `onUpdate`, and `onRefresh` may
handle genuinely separate behavior. `snap` is available when deliberate snapping
is wanted; do not add it merely because a page has scroll animation.

```js
gsap.to(".box", {
  x: 300,
  scrollTrigger: {
    trigger: ".box",
    start: "top 80%",
    end: "bottom center",
    scrub: true
  }
});
```

Selectors in snippets represent targets within the feature's scope. In React,
apply the lifecycle guidance in [react.md](react.md).

## Timeline and pin ownership

Put ScrollTrigger on a top-level tween or on the timeline that owns its child
tweens. A child cannot be controlled independently by both a parent timeline and
its own ScrollTrigger.

```js
const timeline = gsap.timeline({
  scrollTrigger: {
    trigger: panel,
    start: "top top",
    end: "+=1000",
    scrub: true,
    pin: true
  }
});
timeline.to(first, { x: 100 }).to(second, { y: 50 });
```

`panel`, `first`, and `second` are the feature's existing DOM targets. Pin the
stable panel and animate its children, rather than moving the pinned element.
Keep default pin spacing unless the surrounding layout explicitly manages it;
otherwise content can collapse or overlap.

## Horizontal travel driven by vertical scroll

Use this pattern where the track actually overflows its panel. Measure the real
travel distance instead of assuming every child has viewport width. For a
responsive layout, create or revert the horizontal pattern where that overflow
is intended; do not pin a section with no horizontal content to reveal.
`panel` below is the feature's own DOM element, such as its owning ref's
`current` in React. A GSAP context does not scope native `document.querySelector`.

```js
const track = panel.querySelector(".horizontal-track");
const travel = () => Math.max(0, track.scrollWidth - panel.clientWidth);

const scrollTween = gsap.to(track, {
  x: () => -travel(),
  ease: "none",
  scrollTrigger: {
    trigger: panel,
    pin: true,
    start: "top top",
    end: () => "+=" + travel(),
    scrub: true,
    invalidateOnRefresh: true
  }
});

track.querySelectorAll(".item-trigger").forEach(item => {
  gsap.to(item.querySelector(".item-visual"), {
    y: 80,
    scrollTrigger: {
      containerAnimation: scrollTween,
      trigger: item,
      start: "left center",
      toggleActions: "play none none reverse"
    }
  });
});
```

The container animation must use `ease: "none"`. Pinning and snapping are not
supported on triggers that use `containerAnimation`; pin belongs on the outer
driver above. Keep each nested trigger's horizontal position stable while
animating its visual child, or explicitly account for the trigger's movement.

## Standalone and batched triggers

`ScrollTrigger.create()` accepts the same trigger geometry without an attached
tween, for state changes or other scroll-dependent behavior. Its callbacks receive
the instance, including `progress`, `direction`, and `getVelocity()`.

`ScrollTrigger.batch()` creates one trigger per target and collects callbacks
over a short interval. Batch callbacks receive `(targets, scrollTriggers)`, both
arrays. `interval` and `batchMax` control grouping; a function-valued `batchMax`
can adapt on refresh. Batching coordinates callbacks; it is not a scrubbed timeline.

```js
ScrollTrigger.batch(cards, {
  start: "top 80%",
  onEnter: targets => gsap.to(targets, {
    opacity: 1, y: 0, stagger: 0.1, overwrite: true
  })
});
```

`cards` is the scoped collection. Do not pass a single `trigger` to `batch`, or
animation-control options such as `scrub`, `snap`, `animation`, or `toggleActions`.
Batch callbacks run after setup: track the animations they create in the owning
context (for example, React's `contextSafe`) or explicitly dispose those tweens.

## Layout changes, order, and disposal

Call `ScrollTrigger.refresh()` after layout changes that affect measured
positions, including relevant image/font loading and dynamic content. Viewport
resize refreshes automatically. Use functions for geometry that must be measured
again, and `invalidateOnRefresh` when the animation's recorded values must reset.

Create triggers top-to-bottom. If creation order differs, use `refreshPriority`
to restore the required order: a higher number refreshes earlier. This matters
when an earlier pin changes the positions of later sections.

Dispose only this feature's triggers when removing it or changing pages. Use the
owning GSAP context's revert, or retain and kill the individual instances. Remove
owned listeners/ticker callbacks too. Remove development `markers` before delivery.

## Existing custom scrollers

Use `scrollerProxy()` only when the chosen scroller virtualizes/transforms content
so its native coordinates do not describe the visible scroll. A scroller that
retains native coordinates may need only event/ticker synchronization; follow its
official integration recipe first. GSAP ScrollSmoother needs no proxy. This skill
does not require installing a smooth-scroll library.

A proxy's `scrollTop` / `scrollLeft` method distinguishes a setter by
`arguments.length`, so setting zero still works. Provide the actual visible rect
through `getBoundingClientRect` when needed. Notify ScrollTrigger on scroll
updates, and remove that listener on disposal.

```js
// Adapt to the existing scroller's API; this example assumes scrollTop + listeners.
// scrollerElement is its stationary visible viewport, not the transformed track.
ScrollTrigger.scrollerProxy(scrollerElement, {
  scrollTop(value) {
    if (arguments.length) customScroller.scrollTop = value;
    return customScroller.scrollTop;
  },
  getBoundingClientRect() {
    return scrollerElement.getBoundingClientRect();
  }
});
customScroller.addListener(ScrollTrigger.update);
// Owning cleanup: customScroller.removeListener(ScrollTrigger.update).
```

Advanced proxy options include `pinType`, `fixedMarkers`, and scroll dimensions;
choose them from the actual scroller's behavior, not as universal fixes.

See the official [ScrollTrigger reference](https://gsap.com/docs/v3/Plugins/ScrollTrigger/),
[batch](https://gsap.com/docs/v3/Plugins/ScrollTrigger/static.batch()/), and
[scrollerProxy](https://gsap.com/docs/v3/Plugins/ScrollTrigger/static.scrollerProxy()/)
documentation for options not covered here.
