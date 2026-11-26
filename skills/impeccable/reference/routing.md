# Command guidance

## Workflow questions

Give advice without executing workflows; the menu below is only for invocations without a task. Consult relevant command references as needed for prerequisites and scope. Link to the [docs](https://impeccable.style/docs/) for the broader workflow guide. If the user also requests execution, follow that request.

## Review and improve

Start with the user’s requested outcome and scope. For this workflow, reuse applicable findings and verification across references; each reference supplies its method, not another standalone run. A request to review, audit, or suggest improvements returns findings unless it also authorizes edits. A request to improve an existing UI authorizes fixes within that scope. Preserve the established identity, content, and behavior unless the user asks to change them.

1. **Inspect the affected UI.** For a whole site, map its routes, distinct page templates, shared components, and relevant states. Inspect representative pages for each template and record actual coverage and gaps. If editing, capture representative before views where possible. Use [critique](critique.md) when design, usability, or generic patterns are in scope, and [audit](audit.md) for applicable technical checks. Reuse relevant current detector evidence without duplicating scans of the same scope and state. A detector flag calls for judgment; a clean scan does not establish quality.
2. **Apply the methods that match confirmed findings if edits were requested.** Use [typeset](typeset.md) for font roles, scales, and readability; [layout](layout.md) for grouping, alignment, and spacing; [distill](distill.md) for redundant containers and visual noise; [colorize](colorize.md) for color roles and contrast within the identity; [clarify](clarify.md) for unclear interface copy. Read only the references that apply; the other commands remain available when the task calls for them. Fix repeated defects in their shared styles or components. Use consistent spacing for equivalent relationships and keep purposeful differences in hierarchy. Combine changes in one pass and use [polish](polish.md) for final refinement and verification. Hand the current findings directly to that pass instead of reopening a prior report or re-auditing unchanged work.
3. **Verify and report.** For web UI changes, inspect the same affected routes and states after changes at desktop and phone widths. Exercise the affected interactions, verify the design and accessibility details the change touches, and check shared changes on their consumers. Show or link before/after when available. State which routes and states were checked and what could not be verified. PRODUCT.md and DESIGN.md are context; writing them does not complete a UI improvement.

## No-task routing: the context-aware menu

Use this menu only when neither the invocation nor the referenced conversation gives an actionable task. If a task is clear but its target cannot be resolved from context or the project, ask for the target instead of listing commands.

Setup has already run `impeccable context`. If that reported `NO_PRODUCT_MD`, the project has no captured context yet: lead the menu with `/impeccable init` as the top recommendation (one line on why) and still show the rest below; don't silently jump into init. Otherwise run `"<skill-base-dir>/scripts/impeccable" signals` once and read its JSON, then lead with the **2-3 highest-value next commands**, each with a one-line reason pulled from the signals, followed by the full menu (the Commands table in SKILL.md, grouped by category). **Never auto-run a command; the recommendation is a suggestion the user confirms.**

Reason over the signals; there is no score to obey:

- `setup.hasDesign` false while `setup.hasCode` true → `document` (capture the visual system).
- `critique.latest` is `null` → the project has never been critiqued; for a set-up project with a real surface, offering `/impeccable critique <surface>` is a strong default.
- `critique.latest` with a low `score` or non-zero `p0` / `p1` → `polish` (it reads that snapshot as its backlog and closes it when stale or cleared).
- `git.changedFiles` pointing at one surface → scope `audit` or `polish` to those files specifically, naming them.
- `devServer.running` true → `live` is available for in-browser iteration, and `generate` for one-shot variant runs on a named element; if false, don't lead with either. **`live`, `generate`, and the bundled `impeccable detect` are web-only.** If `setup.platform` is `ios`, `android`, or `adaptive`, don't lead with any of them; the browser overlay and the HTML rule engine don't apply to native app code.
- Otherwise group by intent (build new / improve what's there / iterate visually), tailored to the current surface and `setup.platform`.

**If `scan.targets` is non-empty and `setup.platform` is not `ios`/`android`/`adaptive`, run `"<skill-base-dir>/scripts/impeccable" detect --json <scan.targets joined by spaces>` once** (the bundled detector over local files: no network, no npx; it reads HTML/CSS, so skip it for native projects). `scan.via` tells you what they are: `git-changes` (the markup/style files in your dirty tree, the most relevant set), `source-dir` (e.g. `src`, `app`), `html`, or `root`. Fold the hits into your picks: many quality / contrast hits → `audit` or `polish`; a specific slop family → the matching command (gradient text or eyebrows → `quieter` / `typeset`, flat or gray palette → `colorize`, and so on). It's a real, current signal that beats guessing. If detect errors or the tree is large and slow, skip it and recommend the user run `audit` themselves; never block the suggestion on it.

Keep it to 2-3 pointed picks with the exact command to type. The menu stays the fallback; the recommendation is the lede.
