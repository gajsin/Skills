# Project-specific rule examples

Optional examples, not global requirements. Select and adapt only the rules
supported by the project's requirements or the user's instructions. No framework,
library, service, or deployment platform is required merely by this document.

## Frontend

- Keep local state local. Use the project's selected approach for shared state.
  Cache only with a defined update and invalidation strategy.

## Services and production

- Record useful operational events, errors, timing, and request identifiers
  without secrets or noisy repetition. Reuse existing diagnostics and monitoring.
- Define recovery and health checks where service availability requires them.
- Choose build-cache and deployment-cleanup policies for the actual environment.
  Do not delete shared resources or require clean builds without a reason.
- Make substantial migrations staged and recoverable. Cover critical user
  behavior with appropriate integration or end-to-end checks.

## LLM applications

- Use the chosen provider's SDK or the project's existing integration. Introduce
  an orchestration framework only when the workflow needs its capabilities.
- Treat prompts as maintained code: define the task, context, constraints, tools,
  output format, and success criteria. Keep shared prompts in one source of truth.
