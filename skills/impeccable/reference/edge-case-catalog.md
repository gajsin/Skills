# Realistic UI edge-case examples

Use the rows relevant to the requested component. Respect its schema, supported languages, limits, and permitted states. A value the contract rejects belongs in a validation check, not a normal display fixture. Do not expand a narrow task into testing every row.

| Data or condition | Examples | What to inspect |
|---|---|---|
| Names | `J`, `Jo`, `Александра Константинопольская`, `Aleksandra Wiśniewska-Kowalczyk` | Wrapping, initials, row and link size |
| Complex Unicode | `Đặng Thị Ngọc Hân`, `王秀英`, `👩🏽‍💻 Анна` | Font clipping, grapheme-safe initials and truncation |
| Mixed direction | `نور الهدى عبد الرحمن` beside a number or email | Direction and punctuation when supported |
| Missing or duplicate names | Empty/missing optional name; two identical names | Honest empty state and stable identification |
| Unbroken identifiers | `bartholomew.fitzgerald@northwind-industries-holdings.example.com`; UUID; a permitted long URL | Overflow and whether distinguishing parts remain available |
| File names | `Q3 Board Deck — FINAL (revised) v12.pdf` | Wrapping/truncation preserves useful identity and extension |
| Labels | `Benachrichtigungseinstellungen`; a long supported translation | Buttons, badges, and controls grow or wrap |
| User-supplied text | Spaces only; newlines; permitted maximum length; literal `<script>alert(1)</script>` | Empty handling, layout, safe text rendering |
| Numbers | `0`, `1`, `1 000 000`, permitted negative/decimal values | Plurals, precision, signs, and width |
| Missing numeric data | Contract-permitted null or partial response | No raw null/NaN; no invented zero |
| Collections | 0, 1, page-size, page-size + 1; documented maximum | Empty state, pagination boundaries, constrained long-list rendering |
| Live values | Count `99 → 100`; label changes while loading | Width jumps and stable interaction |
| Time | A known instant near midnight in two supported time zones; a permitted future date | Correct date/relative time and boundaries |
| Images | Missing/404/slow image; extreme aspect ratio; transparent logo | Existing missing-media behavior, reserved space, cropping, contrast |
| States | Loading, error, partial data, read-only, no permission | Understandable status, preserved input, permitted actions |
| Environment | Narrowest supported container; 200% zoom; supported theme/RTL/touch | Clipping, reachability, readable text, keyboard and touch access |

Use synthetic data and `example.com`, `example.org`, or `.test` addresses. Trigger failure states through existing mocks or local controls; do not interrupt shared services or delete real data to manufacture a case.

Prefer existing fixtures and the project's test tools. For a one-off check, keep fixture data temporary or within an existing test. A permanent mode switcher, test page, new dependency, or large E2E suite is not required by this catalog; add one only when the task actually needs a reusable facility.

Record the failing value/state, expected behavior, and observed result. Fix confirmed problems only within the authorized scope; report other findings separately. A suitable check of the affected case and a normal case is enough when no concrete risk remains.

## Source

Condensed and adapted from [Emil Kowalski's Break UI catalog](https://github.com/emilkowalski/skills/blob/2d228630ba1446365f614a108cb8252f1feda202/skills/break-ui/CATALOG.md), MIT; see [license](../licenses/emil-skills-MIT.txt). Local adaptation: 2026-10-21. This is a reference for Impeccable hardening, not an additional skill or automatic audit.
