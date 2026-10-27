---
name: model-provider-qualification
license: MIT
description: Qualify an AI model and provider route with evidence when invoked with /model-provider-qualification.
---

# Model/provider qualification

Prove the exact runtime combination at the cheapest faithful seam before exposing a full workload. A model name alone is not the unit being qualified: the model, provider route, payload profile, and pipeline stage form one runtime combination.

## Non-negotiable gate

Do not start a full paid pipeline test or deploy a model change until all of these are known:

1. The working reference path and its exact observable behavior, or explicit acceptance criteria for a first integration without one.
2. The candidate's documented parameter semantics and live provider metadata.
3. A cheap canary has exercised the real prompt, one representative real input (including an image when used), and the real tool contract when the pipeline uses tools.
4. Every provider that may receive traffic is qualified, or routing is restricted to providers that are.
5. Functional behavior, latency, and usage are compared with the reference or agreed acceptance bounds; unexpected regressions or missing comparison evidence are reported.

A successful HTTP response is not qualification. A response that calls a tool but silently uses expensive default reasoning, takes far longer than the reference, or came from an untested provider is still a failed gate.

## Establish the reference

Trace the nearest working production path end to end when one exists. For a first integration, state that no production reference is available and use an agreed request/response contract and acceptance criteria as the baseline. Apply comparisons and immutability checks only to reference paths that exist; do not invent production evidence.

Capture the relevant baseline details without exposing secrets:

- exact outgoing payload fields and values;
- actual response provider, model, and finish reason;
- reasoning or thinking configuration;
- tool choice, parallel tool behavior, and schema mode;
- image form, per-file size, total image volume, and history pruning;
- number of model turns, latency per turn, retries, and usage or cost;
- checkpoint and failure behavior.

When the user says "like the current model," these observations are the compatibility baseline. Preserve its path unless the user approves a deliberate change.

## Build the compatibility matrix

Use current official model documentation, gateway documentation, live metadata, project configuration, and production logs. For each candidate model and provider route, record:

- image and tool support;
- accepted `tool_choice` values and whether tool use can be required;
- reasoning or thinking defaults, allowed levels, disable syntax, and what omission means;
- support for strict schemas, parallel tool calls, seed, and output limits;
- context, image download, per-file, and total request limits;
- rate limits, timeouts, routing, and fallback behavior.

Treat an omitted reasoning parameter as unknown until documentation or a canary proves its effect. Do not infer that omission disables thinking. Treat aliases such as `medium` as unknown until their provider-specific mapping is verified.

Automatic routing expands the matrix. If a gateway can choose three providers, all three are unqualified until tested. Prefer a proven pinned provider when the gateway cannot guarantee that every fallback accepts the same payload.

## Qualify cheapest first

Run in this order:

1. Static payload tests: assert the exact candidate payload and verify that any existing reference payload is unchanged.
2. One paid canary: production prompt, one representative real input, a real tool when used by the pipeline, and the intended reasoning setting.
3. Minimal multi-turn canary when the pipeline depends on repeated tool calls or growing history.
4. Provider-route and fallback checks for every route that remains enabled.
5. Full pipeline smoke test only after the earlier checks pass.

Use an existing explicit authorization for paid calls. Otherwise obtain approval and state the planned request or spending cap before the first paid call. Stop the sequence when a gate fails; do not use a full catalog to discover parameter defaults.

For every live attempt record the effective outgoing profile, actual provider, latency, retry count, finish reason, and usage or cost. Compare these with the reference immediately. Unexpected latency or usage ends the paid sequence until its cause is understood.

## Classify failures before retrying

Separate these cases:

- model capability or parameter incompatibility;
- provider-specific incompatibility;
- transient transport failure or rate limit;
- application or pipeline defect.

Retry only errors classified as transient, using a bounded policy. A generic provider `400` is provider-specific evidence: exclude or switch that provider rather than repeating the same unpinned request and hoping routing changes. Record the provider on both successful and failed attempts.

Preserve recoverable state and report the failed gate. Do not weaken tools, prompts, image evidence, or acceptance checks merely to obtain a green response.

## Keep the implementation contained

Keep compatibility profiles inside the owning client or configuration seam. Prefer a small data profile over scattered model-name branches. Unknown future models begin unqualified and use only the documented conservative base payload; they do not inherit claims made for another model.

The architecture may guarantee a consistent pipeline contract. It cannot guarantee equal reasoning quality across models. Diagnose unequal inputs or tool evidence as an integration problem; report worse results under equal inputs as a model-quality result.

## Completion criterion

Qualification is complete only when any existing reference remains unchanged, the candidate meets the explicit acceptance criteria and faithful canaries within accepted time and usage bounds, every enabled provider route is accounted for, focused tests pass, and the report separates observed facts from remaining uncertainty.
