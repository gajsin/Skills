---
name: ponytail
description: Prefer reuse and minimal complete code when explicitly invoked with /ponytail.
license: MIT
---

# Ponytail

Solve the complete requested task with the smallest clear, correct change. Be
efficient about the solution, never careless about understanding or finishing it.

## Mode

Active for the session after explicit invocation, until `/ponytail off`,
"stop ponytail", or "normal mode". Default: **full**.
Switch with `/ponytail lite|full|ultra`. Reading or editing this skill is not activation.

## Before editing

Read the request and trace the affected behavior, its owning code, and relevant
callers, tests, fixtures, configuration, and exports. Check what must remain unchanged,
including protected data and public behavior. A bug fix addresses the root cause at
the owning seam; inspect affected callers before changing shared code.

## Choose the smallest complete solution

Take the first option that satisfies the requirements:

1. Skip speculative features, options, and flexibility.
2. Reuse a suitable project helper, component, or established pattern.
3. Use the standard library or native platform.
4. Use a suitable dependency already installed. Do not add a package for a few lines.
5. Write only the missing implementation. Prefer a clear expression; keep named
   steps when they improve readability or correctness.

- Complete every required part, including callers and tests affected by the change.
  Do not substitute a partial result or ask the user to request missing work again.
- Preserve suitable project structure. Add an abstraction, wrapper, conversion,
  configuration, or layer only for a demonstrated need. Keep interfaces small and
  complexity local; deletion is useful only when required behavior survives.
- Preserve validation, error handling, useful diagnostic logging, security,
  accessibility, protections against data loss, and required real-world configuration.
- Between equally simple options, choose the one that handles the relevant edge cases.
- A deliberate simplification with a known limit must satisfy current and confirmed
  future requirements. When the limit matters, record `limit: <ceiling>; <upgrade
  condition>`. Do not ship a workaround a known next step must discard.
- Explain scope or correctness decisions when needed. Continue within authorization;
  ask only when an unresolved decision materially changes scope or correctness.

## Verify and finish

Choose checks proportionate to the changed behavior and risk. Reuse existing tests,
fixtures, and tooling; keep required repository gates. Add a focused regression check
when relevant risk lacks coverage. Low-risk documentation or metadata may need only
inspection. Do not add a new framework or inline self-check when existing checks
suffice. Stop after sufficient verification; repeat only for a new change, failure,
or concrete remaining risk.

Report the result, relevant verification, and material limits concisely. Give the
detail the user requested. This mode limits implementation complexity, not the
thoroughness of the work, requested explanation, or the quality, states, and
checks required by an active domain skill such as Impeccable or GSAP.

## Levels

- **lite:** build what was asked; mention a materially simpler alternative briefly.
- **full:** apply the rules above. Default.
- **ultra:** also challenge speculative additions; fulfil confirmed requirements,
  preserve safeguards, and keep the code readable.

Adapted from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/tree/09c434a), MIT.
