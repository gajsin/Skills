# Choosing and Combining Skills

Choose the skills needed for the user's current task and stage. A skill supplies a
method, not permission for extra work. Tagging every skill does not mean running
every workflow.

## Invocation and context

- **Codex:** `$name`; the pack's skills set `allow_implicit_invocation: false`.
- **Claude Code:** `/name`; the pack's skills set `disable-model-invocation: true`. Stack
  skills at the start of the message, for example
  `/architecture-first /ponytail /spec-review Implement the agreed feature`. In the
  terminal one message expands the first skill and up to five more; through the
  Agent SDK or `claude -p` only the first expands. A `/name` after plain text is not
  loaded directly; it only permits Claude to invoke that skill in this message.
- **Antigravity:** `/name` is the intended invocation. Manual-only wording is a
  preference, not a documented technical prohibition on automatic selection.
- Instructions are English; interviews, explanations, and deliverables use the
  user's requested language.
- Load supporting references only for the requested branch. Invoking every skill spends
  more context and can mix incompatible deliverables; it does not improve every task.

## What each skill is for

| Skill | Use when | Result | Changes and boundaries |
|---|---|---|---|
| `grilling` | Project requirements or consequential decisions are unclear | Adaptive interview, agreed scope and acceptance criteria | No implementation; save a specification or plan only when requested |
| `architecture-first` | Changing a substantial part of an existing system | Traced behavior, minimal design, authorized implementation and review | Only the requested stage and change; not a mandatory process for every small edit |
| `codebase-design` | Module interfaces, dependency seams, or testability need a decision | Interface proposals; an evidence-backed architecture audit | Audit/proposals do not implement themselves |
| `ponytail` | Keep coding changes minimal and complete | Session mode for simpler implementation | Does not remove required behavior, quality, states, or checks |
| `spec-review` | Review changes or audit an existing project | Separate Standards and Spec findings plus scoped tool evidence | No unrequested fixes or project dependency changes; report missing checks explicitly |
| `diagnosing-bugs` | A hard bug or performance regression has an unknown cause | Reproduction loop, root cause, focused fix and regression evidence | Diagnosis/fix within the request; stop for missing reproduction access rather than invent evidence |
| `retro` | An agent session produced avoidable failures | Evidence, causes, and proposed corrections | Report/proposals; no automatic rule, hook, or memory edits |
| `caveman` | Short, dry, grammatical agent replies | Session mode for concise wording | Preserves requested depth, facts, uncertainty, and required outputs |
| `humanizer` | Write, edit, or summarize prose from supplied facts and context | Natural text in the intended voice | No setup form; preserve relevant facts and material limits; only authorized file edits |
| `impeccable` | Build, assess, or refine a UI | Depends on the selected command | Build/refine edits the UI; critique/audit assess it and may write review artifacts |
| `gsap-react` | GSAP is selected for React/Next.js | Scoped setup, lifecycle handling, and cleanup | No migration of a suitable existing stack just because the skill was invoked |
| `gsap-scrolltrigger` | GSAP is selected for scroll-linked animation | ScrollTrigger implementation and layout/cleanup checks | No dependency or smooth-scroll library is implied by the invocation |
| `logo-interview` | Find a logo direction through an interview and visual comparison | Agreed brief, viewed moodboard/direction, authorized studies or exports | Preserve originals and decision levels; no automatic site changes |
| `model-provider-qualification` | Add or change an LLM model/provider route | Compatibility evidence, faithful canaries, qualification verdict | Scoped tests/integration; paid calls need existing authorization or an agreed cap; no automatic full paid run or deployment |

## Engineering skills with different jobs

- **Architecture First — how to make this change.** Trace the existing path,
  preserve required behavior, choose the smallest supported design, implement only
  what is authorized, then verify.
- **Codebase Design — where behavior belongs and what callers see.** Explore an
  interface or seam when that decision is unresolved. It supports Architecture
  First; it does not require a parallel redesign or new abstraction.
- **Ponytail — how much mechanism is necessary.** A session mode, not an extra
  design or review pass. Apply its smallest-complete-solution rule throughout.
- **Spec Review — whether the changes satisfy standards and the request.** It
  can inspect the current agent's work, someone else's diff, or an existing project.
  It does not need to have led the implementation.

They can be invoked together for the same change. Reuse the same acceptance
criteria, trace, and evidence; do not produce a separate implementation for each skill.
When Architecture First and Spec Review cover the same diff, run one
standards/spec review through Spec Review. The main agent still verifies findings.
Keep Impeccable's distinct visual review and required runtime checks.

For a tiny, understood fix, Ponytail and a focused check may be enough. Do not
invoke a full architecture workflow or independent reviewers merely to change a
few safe lines. Risk, not line count, determines the necessary scrutiny.

## Automated evidence in Spec Review

Invoke `$spec-review Audit the entire project.` for an existing-system audit,
including when there are no changes. A change review keeps the requested diff as
its boundary. The user does not need to name Crapper, Dryer, or Mutator.

Spec Review accounts for their applicable evidence and reports what ran, what did
not, and why. Tool setup uses a dedicated cache, not project dependencies. Crapper
and Dryer inspect code; Mutator site discovery is separate from executing mutation
tests. The supplied runtime includes native Windows compatibility and retains the
upstream POSIX behavior. Actual execution uses an independent snapshot and the
project's verified test command. A scan, missing
coverage, a metric, or an exit code does not establish correctness. Tools supplement
the reviewer's work on requirements, architecture, and behavior.

## Other overlaps

- **Architecture First + Diagnosing Bugs:** for a hard bug, the diagnostic loop
  satisfies Architecture First's reproduction gate. Honor Diagnosing Bugs' stop
  condition if no loop can be built; do not build a second harness for the same bug.
- **Grilling + Logo Interview:** Logo Interview leads a logo-specific interview.
  Reuse its settled answers; do not start a second generic questionnaire. Use
  Grilling separately for unresolved product requirements outside that interview.
- **Impeccable + GSAP:** Impeccable handles visual intent and UI quality. GSAP
  skills handle the selected animation technology. Use both GSAP skills for
  scroll-driven animation in React; neither forces GSAP onto another suitable stack.
- **Caveman + Humanizer:** Caveman shortens replies and requested prose while
  preserving meaning and the appropriate tone. Humanizer makes the wording natural
  for its reader. A warm or detailed document remains warm or detailed when requested;
  concise reporting does not flatten the document.

## Writing without extra setup

One invocation and the task are enough: `$humanizer $caveman Briefly describe what
we did this session.` No mode selection, style form, or writing sample is required.
Use the conversation for facts and the intended recipient for tone. A session
summary needs no invented greeting or recipient; an unfamiliar external business
recipient gets respectful wording (Russian «вы»), while an established «ты» stays.
Short summaries select relevant outcomes but retain material failures and limits.
Caveman removes unnecessary wording without turning the text into fragments or
changing its voice. No fixed percentage of token or cost savings is promised.

## Boundaries when combining

1. The user's requested action controls the work. "Review only" or "propose"
   stops at findings or proposals; implementation-oriented companion skills supply
   criteria, not permission to edit.
2. Resolve prerequisite decisions once. Reuse existing answers and approvals.
   A required answer still blocks dependent work; tags do not replace confirmation.
3. Apply only relevant branches. An unrelated logo, model, animation, or prose
   workflow stays inactive for a backend bug or folder cleanup.
4. Preserve each relevant quality gate, but reuse equivalent evidence and do not
   duplicate the same review. Different visual, behavioral, and standards checks
   are not interchangeable.
5. Report-only means no automatic product fixes. Some tools, especially Impeccable
   critique, normally save snapshots, screenshots, or other review artifacts. Honor
   an explicit no-write restriction and disclose any resulting workflow limit.
6. When instructions truly conflict or the requested stage is unclear, name the
   specific conflict and resolve only that decision. Do not silently expand scope.

There is no guarantee that loading all instructions simultaneously is conflict-free
or makes an agent reliable. Prefer a relevant combination with a clear request.

## Example requests

Examples use Codex's `$`; replace it with `/` in Claude Code or Antigravity.

| Task | Example |
|---|---|
| Small, understood change | `$ponytail Fix the named behavior; preserve everything outside it.` |
| Clarify a new feature | `$grilling Interview me about this feature. Do not implement it yet.` |
| Choose module boundaries | `$codebase-design Compare interfaces for this subsystem; proposals only.` |
| Substantial feature | `$architecture-first $ponytail $spec-review Implement the agreed feature and review the resulting diff.` |
| Review someone else's work | `$spec-review $codebase-design Review this branch against the attached spec. Do not edit files.` |
| Audit an existing project | `$spec-review Audit the entire project against its requirements and standards; report findings without fixes.` |
| Hard bug | `$diagnosing-bugs $ponytail Reproduce and fix this failure. Add Architecture First if the fix requires a substantial design change.` |
| UI audit | `$impeccable audit the checkout form; report findings without product fixes.` |
| Scroll animation in React | `$gsap-react $gsap-scrolltrigger Implement this agreed animation using the existing GSAP setup.` |
| Logo direction | `$logo-interview Help me find a logo direction through an interview and visual board.` |
| Edit prose | `$humanizer Make this text natural; preserve its facts and voice.` |
| Short session summary | `$humanizer $caveman Briefly describe what we did this session.` |
| Provider change | `$model-provider-qualification Qualify this route within the agreed request cap before the full paid run.` |
| Learn from a failed session | `$retro Review this session and propose the smallest corrections; do not change instructions.` |

A possible feature sequence is interview → interface design if needed →
implementation → review. Use only the stages needed for the task.
Use `$caveman` or `$ponytail` as session modes where useful; `off` ends either mode.

## Verification limits

This pack has static consistency and packaging checks. Those checks do not prove
successful behavior on every real task. Native questions, delegation, browsing,
image generation, and runtime checks depend on the active host and permissions.
Keep each host's intended Impeccable build; differing author design bans are not
automatically a synchronization error.
