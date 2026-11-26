---
name: retro
description: "Review an agent session and propose minimal evidence-backed improvements when explicitly invoked with /retro."
license: MIT
---

# Agent Session Retrospective

Review the requested session and propose changes that address demonstrated failures.
Use the user's language.

## Examine the session

Read the original request, material clarifications, agent actions, changed artifacts,
and verification results. State any limit in the available history. Compare the
request with the outcome; support each material discrepancy with evidence and
distinguish established causes from hypotheses.

Separate missing information or access, ambiguous or conflicting instructions,
failure to follow an existing instruction, insufficient verification, and
unjustified scope expansion.

## Propose the smallest correction

Check for an existing rule, tool, or project check before adding anything. Prefer
an existing automated check for mechanically detectable mistakes. Do not duplicate
an instruction that already covers the problem. The main agent remains responsible
for requirements and quality; independent review supplements that responsibility.

## Decide where a correction belongs

Write a concrete action with a clear stopping condition. Keep each rule in one
appropriate place and load conditional detail only when relevant:

- A lasting rule across projects belongs in the user's global AGENTS.md or GEMINI.md.
- A project-specific requirement belongs in that project's instruction file.
- An occasional procedure belongs in an explicitly invoked skill.
- A mechanical condition belongs in an existing linter, test, or CI check.
- A stable user or project fact belongs in host-supported memory when appropriate.

Propose a new hook or mechanism only for a demonstrated need. Prefer clarifying or
replacing an existing rule over adding another. Preserve necessary prohibitions and
permission boundaries; ground general recommendations in the reviewed evidence.

## Deliver

Use a concise table: failure, evidence, cause, proposed correction. Prioritise useful
changes. "No additional instructions needed" is a valid outcome.

Finish with proposals. Editing files, configuring the environment, and publishing
require authorization for those actions.
