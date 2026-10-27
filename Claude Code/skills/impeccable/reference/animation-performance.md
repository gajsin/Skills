# Diagnose web-animation jank

Read only when the scoped web animation stutters, drops frames, or has a concrete performance risk. Keep Impeccable's visual rules and the requested behavior.

## Find the cause

Identify the affected element, trigger, animated properties, driver, and when it becomes slow. A frame has about 16.7 ms at 60 Hz or 8.3 ms at 120 Hz for all required work.

| Symptom or evidence | Investigate | Possible focused change |
|---|---|---|
| Layout work during movement | Animated dimensions, offsets, margins; alternating DOM reads and writes | Batch reads/writes; use transforms when layout and text behavior stay correct |
| Animation stalls during navigation, hydration, or data processing | Main-thread long tasks; a JS-driven animation competing with them | Reduce the blocking work or use an eligible CSS/WAAPI animation within the existing stack |
| A hand-written React animation renders each frame | State updates in rAF, pointer, drag, or scroll callbacks | Keep the visual update in an existing motion value or ref; retain state for meaningful application changes |
| Drag slows as descendants increase | Frequent updates to an inherited CSS custom property | Check style recalculation; write a local transform if descendants do not need the value |
| Motion transform shorthands stall under load | Installed library version and whether that path uses JS/CSS variables or native animation | Test a full transform string only if it preserves transform composition and behavior |
| Blur, shadows, or masks cost too much | Effect area, layer size, repaint cost, target browser | Reduce the affected area or effect cost while preserving the intended design |
| Unrelated properties move unexpectedly | `transition: all` | Name the intended properties explicitly |
| A layer promotion or memory problem remains | Layer count, paint cost, startup/end artifacts | Trial a narrowly scoped `will-change` only with evidence; remove it if ineffective |

These are hypotheses, not automatic replacements. `transform` and `opacity` are useful defaults; layout animation can be appropriate. `scale()` changes rendered content and does not reflow siblings, so it is not equivalent to changing padding or dimensions. Likewise, `opacity: 0` alone does not remove focusability or hit targets. Preserve accessibility and interaction semantics.

CSS/WAAPI can run eligible animations off the main thread; eligibility depends on properties, browser, and library version. Do not promise hardware acceleration. Keep percentage transforms when required for unknown dimensions. Do not impose a universal blur-radius threshold or replace the animation library just for this audit.

## Verify and finish

- Start with the affected path and available evidence. Use a short performance recording for a runtime claim; compare the same interaction and conditions before and after.
- Browser tools or a relevant device check are warranted when needed to resolve the observed jank. Desktop CPU throttling does not reproduce a phone GPU. State device/browser limits; unavailable hardware is a limitation, not a reason for an open-ended investigation.
- Report the cause, location, focused change, measured result, and remaining uncertainty. With code inspection alone, label the cause as a hypothesis and do not claim a measured speedup.
- For an audit, report findings; for a requested fix, apply the smallest supported correction. Stop when the scoped problem is sufficiently checked. Do not add a benchmark system or dependencies without a concrete need.

## Sources

Adapted from [Emil Kowalski's animation-performance](https://github.com/emilkowalski/skills/blob/2d228630ba1446365f614a108cb8252f1feda202/skills/animation-performance/SKILL.md), MIT; see [license](../licenses/emil-skills-MIT.txt). Local adaptation: 2026-10-21.

Version-sensitive details were checked against [Motion's performance guide](https://motion.dev/docs/performance), [MDN on will-change](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/will-change), and [web.dev's animation guide](https://web.dev/articles/animations-guide). Consult current documentation when a library or browser detail determines the fix.
