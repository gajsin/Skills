# Audit an Existing Architecture

Investigate the requested area and propose improvements supported by the actual
codebase and confirmed requirements. Use the user's language.

## Scope

Start with the named problem or subsystem. If none is specified, use known pain
points, the confirmed roadmap, and change history to choose priorities. Read the
affected paths, existing architecture decisions, and checks. Distinguish an observed
problem from a hypothetical risk.

## Find candidates

Look for changes that require coordinated edits across many files, implementation
details leaking into callers, or important behavior that is hard to verify. Apply
the main skill's principles. Small modules, several files, or the absence of an
abstraction do not prove a problem.

For a broad audit, an independent investigator may help when collaboration is
available and authorized. Verify their findings against the source yourself.

## Evaluate

For each candidate, identify the affected files and concrete problem, supporting
code or test evidence, the smallest proposed change, its benefit, cost and risk,
and why it improves on keeping the current design. Respect existing decisions and
constraints; flag a material disagreement with an accepted decision explicitly.

## Report

Present a short table ordered by usefulness. Add a diagram when it clarifies the
code; create an HTML report only when requested. If no convincing candidate exists,
say so.

The audit does not edit code, tests, documentation, or dependencies. The user chooses
the next work after the report.
