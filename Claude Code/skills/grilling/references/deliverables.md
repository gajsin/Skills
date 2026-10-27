# Requested specification or task plan

Read only when the user asks to save interview results, write a specification, or
break an agreed project into tasks. Keep the existing document or tracker when one
already owns the work; do not create a second source of truth.

## Specification

Write a document proportionate to the project, using settled answers and verified
source material. Include what is needed from:

- Problem, users, outcomes, and representative scenarios.
- Agreed behavior, business rules, data or interface contracts, and constraints.
- Scope and exclusions; explicit assumptions and knowingly deferred decisions.
- Define ambiguous terms when needed. For a consequential decision, record the
  chosen option, considered alternatives, and reason. Reuse project documentation;
  create a separate glossary or ADR only when requested.
- Concrete acceptance criteria and how to verify them.

Do not invent requirements, force an extensive user-story list, or turn a hypothesis
into an agreed decision. Include paths or exact technical contracts when they improve
execution; indicate version or freshness where necessary. Preserve the user's source
request. Use their requested filename and format or the existing project convention.

## Task plan

Split agreed work into independently verifiable outcomes. Prefer thin complete paths
through the layers involved in a feature when useful; a documentation or migration
task need not manufacture UI, API, and database work. Show dependencies, scope, and
observable acceptance criteria. Reuse existing architecture and checks.

For each task, capture: desired result, necessary context or source pointers,
dependencies, boundaries, and a verification command or concrete scenario. If the
user requested files, write them in the existing task location or an agreed one.
Creating external issues requires authorization for that action. Saving a document
does not authorize executing its implementation plan.
