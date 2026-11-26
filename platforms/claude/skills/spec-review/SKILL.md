---
name: spec-review
license: MIT
description: Review changes or audit a project against standards and requirements with scoped automated evidence.
argument-hint: "[changes, branch/PR, or project audit] [spec path]"
disable-model-invocation: true
---

Target: $ARGUMENTS

Two-axis review of requested changes or an audit of an existing project:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

Review and report; do not modify the reviewed files unless fixes are already
authorized as part of the task. Companion skills supply review criteria, not
permission to implement.

Assess both axes. Review directly for a localized low-risk diff; use independent parallel reviewers when they materially reduce an identified risk or the user explicitly requests them.

Use the project's issue tracker when one is configured. A missing tracker setup does not block a review; use the user's request, PR description, or local spec as the behavior source when available.

## Process

### 1. Define the scope and comparison

Infer scope from the request. An explicit whole-project audit reviews the existing
system even when there is no diff; a branch, PR, or change review uses a fixed
comparison. If neither is specified, use current work-in-progress changes when
present; otherwise ask which project or comparison to review.

For a project audit, inventory the owned source, relevant tests, configuration,
and requirements. Include relevant untracked work and state exclusions such as
vendor code, generated output, caches, secrets, or unavailable components. Select
representative flows and module boundaries to inspect; a metric report alone is
not a full-project audit. State the source snapshot, inspected files/flows, and
remaining unreviewed scope. The diff-specific
commands below apply only to a change review.

Choose the comparison that matches the request. Use an explicitly supplied ref for its requested role, either as a snapshot or as the base branch for a branch/PR review. Resolve the refs and record the exact diff command and endpoints in the report.

- For a comparison of committed snapshots, use `git diff <ref> HEAD`.
- To review changes introduced by a branch or PR, use `git diff <base>...HEAD` from the merge base. Use the default branch when no base is given. Note the branch commits with `git log <base>..HEAD --oneline`.
- For work in progress, use `git diff <ref>` for tracked changes, defaulting to `HEAD`. Include relevant untracked files as described below.

Before going further, confirm any chosen ref resolves (`git rev-parse --verify <ref>`). For work in progress, inspect `git status --short` and enumerate untracked paths with `git ls-files --others --exclude-standard`. Include the contents of relevant new files even when the tracked diff is empty; leave unrelated and ignored files outside scope and do not stage files just to review them. Confirm that the selected review input is non-empty, and state any exclusions.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. A spec path the user explicitly passed as an argument.
2. The user's request or PR description, followed by issue references in commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.) when an issue tracker is available.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If no behavior source exists, skip the **Spec** axis and report "no spec available". Ask for a spec only if the user explicitly requested a spec comparison.

### 3. Identify the standards sources

Use `~/.claude/CLAUDE.md`, the project instructions loaded by Claude Code
(`CLAUDE.md`, `AGENTS.md`, or both), and standards such as
`CODING_STANDARDS.md` or `CONTRIBUTING.md`. Respect their precedence and the
user's requirements.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; assess it within the selected scope:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

- **Dead Code** (local addition): unused or unreachable code, abandoned debug output, or temporary files left in the changed path. → report removal after confirming that no caller or required behavior depends on it.
- **Silent Fallback** (local addition): a catch, default, or alternate path that conceals a failure or substitutes an invalid result. → surface the failure; preserve recovery that belongs to the agreed behavior and keeps its guarantees. Ordinary optional defaults and valid empty results are not failures by themselves.

### 4. Collect applicable automated evidence

The user need not list tools. For supported source code, read
[automated-checks.md](references/automated-checks.md) and use the shared inspector
for Crapper complexity/coverage evidence, Dryer duplicate candidates, and Mutator
site discovery. Apply the reference's separate execution gate when actual mutation
testing is justified. Reuse current project checks and verified evidence.

Account for each tool in the report: performed with results and limits, not
applicable with a reason, or not performed with a reason. A missing runtime is not
"not applicable". Mutation-site discovery is not mutation testing. No installation
or test failure, unknown coverage, empty selection, or exit code alone is a pass.
Documentation-only work needs no analyzer setup. Keep checks within the requested
scope and host permissions; do not alter reviewed code or project dependencies.

### 5. Choose direct or independent review

Risk takes precedence over line count. Security, permissions, persistent data,
migrations, concurrency, public contracts, or substantial cross-module behavior can
justify independent review even in a short diff. A localized low-risk change needs
self-review only; run Standards and Spec separately with the briefs below.

When independent review is justified and available, launch the two axes in parallel
as two non-fork `Agent` calls with self-contained input packets. For source-only
review, use a read-only role such as Explore when available and pass the applicable
rules explicitly. Collect both completion results before aggregating. Honor the
user's reviewer count and delegation limits. If collaboration is unavailable, assess both axes yourself
and disclose any material limit. A missing spec still skips only the Spec axis.

**Standards sub-agent prompt** should include:

- The source snapshot and selected files/flows; for changes, the full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full (the sub-agent has no other access to it).
- The brief: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** should include:

- The source snapshot and selected files/flows; for changes, the diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 6. Aggregate

Verify reported findings against the reviewed source and applicable requirements. For a project audit, use the selected files and flows wherever the reviewer briefs refer to a diff. Remove unsupported claims or identify unresolved uncertainty. Present confirmed findings under `## Standards` and `## Spec`, retaining their evidence. Keep the axes separate; strength on one axis does not cancel a failure on the other (see _Why two axes_).

For a security finding, trace the untrusted entry point through the controls that
actually run to the unauthorized effect. Identify who can reach it and what
changes or is exposed. If the conclusion depends on an unverified configuration or
runtime fact, state that fact and mark the finding as unconfirmed.

Add a compact tool-evidence table with scope, result, and limits for Crapper, Dryer,
and Mutator; explicitly distinguish a mutation scan from executed tests.

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes: that's the reranking the separation exists to prevent.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
