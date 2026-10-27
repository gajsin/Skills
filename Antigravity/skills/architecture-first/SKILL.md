---
name: architecture-first
license: MIT
description: Trace the current path and choose the smallest supported design when invoked with /architecture-first.
---

# Architecture First

Choose the simplest evidence-backed design at the right seam. Understanding is
mandatory; neither copying nor replacing existing architecture is a substitute for
evaluating it. Apply only the stage the user requested: analysis, design, or
review does not authorize implementation. Reuse settled interview decisions.

## Non-negotiable rule

Do not edit until you can state all three in concrete terms:

1. **Current path** — the real end-to-end flow, including callers, data sources,
   transformations, side effects, tests, configuration, and production evidence.
2. **Reference path** — the nearest working implementation or established project
   pattern. When the user says “like X” or “do it as X,” X is the behavioral
   compatibility baseline and primary evidence, not automatically the best
   architecture.
3. **Required delta** — only the behavior that must differ from the reference path,
   plus the invariants and files that must remain untouched.

If any item is unknown, investigate it before proposing a design or changing code.
Preserve the reference path's observable behavior and required invariants by default.
Reuse its internal design only where it fits the new problem.

## Evidence gate

- Separate observed facts from hypotheses. Read code, configuration, tests, and real
  logs or data when the task depends on runtime behavior.
- Reproduce the reported failure before fixing it when reproduction is safe and
  possible. Reuse an existing regression check or add one that fails for the real
  reason when changed behavior needs coverage. If reproduction is unavailable, name
  the missing evidence and choose the best available verification. When
  diagnosing-bugs is active for this bug, reuse its feedback loop and honor its
  stop condition when no loop can be built; do not create a second loop.
- Test one hypothesis at a time. Remove abandoned experimental code before testing
  the next hypothesis.
- Before a third failed hypothesis, stop editing, remove only your failed
  experimental changes, and trace the reference path again. Preserve pre-existing
  and user-owned changes. More patches are not more evidence.

## Design gate

Apply the Ponytail ladder only after the trace is complete:

1. Start with the working path and evaluate whether its owning seam fits the change.
2. Reuse a suitable helper or pattern already in the project.
3. Use the standard library or native platform.
4. Use a suitable dependency already installed in the project.
5. Add the minimum new implementation only when the earlier rungs cannot satisfy the
   demonstrated requirement.

Prefer replacement at the owning seam over a parallel layer around it. Preserve a
small interface and keep complexity local. Every new mechanism must map to an explicit
requirement, a reproduced failure, or a demonstrated improvement over reuse.
Meet the confirmed roadmap and production constraints without implementing future
features outside the requirements. Avoid temporary architecture that a known next
step must discard.

A different architecture is valid when a concrete comparison shows that it materially
improves correctness, simplicity, maintainability, safety, or operating cost while
preserving the requested behavior. State the alternatives and tradeoffs before
implementation. Use the better design directly when the difference is small and
within scope; get the user's direction when the divergence materially changes scope,
cost, persistence, interfaces, or external behavior.

Treat these as **critical design decisions**: a new source of truth or persistent
store; a parallel pipeline; another model, agent, judge, validator, retry stage, or
background process; a new fallback path; a new dependency or public interface; a broad rewrite; modifying
the known-good reference path; or changing semantics to force a target metric. Make
such a decision only after comparing it with reuse against the explicit requirements
and the criteria above. If the new design is not clearly better, reuse the existing
seam.

Verification of changed behavior, validation at trust boundaries, explicit error
handling, required diagnostics, security controls, accessibility, and protections
against data loss are safeguards, not optional complexity.

## Implementation loop

1. Record the request’s acceptance criteria, no-touch areas, and protected data.
2. Trace the current and reference paths end to end.
3. Produce a one-sentence design: “Preserve behavior X; implement through Y; leave Z
   untouched.”
4. Choose the smallest meaningful verification for the changed behavior and risk.
   Reuse existing checks; add a failing regression check when coverage is missing.
   A low-risk documentation or metadata edit may be verified by direct inspection.
5. Edit the owning seam. Avoid event-specific rules, duplicated pipelines, speculative
   abstractions, and compatibility layers without a real caller.
6. Run the focused check, affected tests, and the repository’s required gates.
   Repeat checks to resolve a failure, a further change, or a concrete remaining risk.
7. Inspect the final diff against the one-sentence design. Remove unrelated changes
   you introduced; preserve pre-existing and user-owned edits. When staging is
   authorized, use an explicit allowlist in a worktree with protected changes.

## Review and release gate

When spec-review is also invoked for this change, use it for the standards/spec
review below; do not launch a duplicate set of reviewers. This does not replace
a domain skill's distinct visual or runtime checks.

First review the full diff yourself against both questions:

- **Architecture/spec:** Does the diff preserve the required reference behavior and
  use the best-supported design without scope creep or an unjustified second system?
- **Code/standards:** Is the implementation correct, minimal, tested, free of dead
  code and hidden fallbacks, and compliant with repository instructions?

Use independent read-only reviewers when the user explicitly asks for them, or when
another perspective materially reduces an identified risk: cross-module behavior,
security or permissions, persistent data, migrations, concurrency, or a public
contract. A localized low-risk edit needs self-review only. Risk takes precedence
over line count; many changed files alone are not a reason to delegate.

When delegation is justified and available, separate architecture/spec from
code/standards in two parallel reviews when both apply. Supply self-contained inputs
and verify each finding yourself. Respect an explicit request for no delegation or
a particular reviewer count. If collaboration is unavailable, perform both reviews
yourself and disclose any material verification limit.

Resolve blocking findings and rerun the relevant checks. Obtain the reviewers' final
verdict when reviewers were used. Review does not authorize commit, push, deployment,
scope expansion, or redesign; follow the user's existing authorization.

## Honest stopping condition

If real evidence still misses the requested outcome, report the exact mismatch. Do not
make tests weaker, fabricate coverage, tune logic to one example, or add architecture
merely to make a metric look successful. Offer the smallest next decision. If the user
explicitly directs shipping the current state, freeze the design, run the release gate,
and disclose the remaining mismatch.

The completion criterion is not “code was written.” It is: the requested delta works,
the reference behavior is preserved or deliberately superseded with approval, the
required checks pass, the final diff contains no unexplained mechanism, and any known
mismatch is explicit.
