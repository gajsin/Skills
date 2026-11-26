# impeccable hooks

Run the resolved launcher with `detect [target]` when `context` reports `MANUAL_DETECTOR_REQUIRED` or the workflow calls for a scan and no working detector hook is active. `hooks status` reports configuration. An `enabled` value alone does not prove a hook is installed or firing.

Where an automatic detector hook is configured, it scans direct edits to design-relevant files (`.tsx`, `.jsx`, `.html`, `.vue`, `.svelte`, `.astro`, `.css`, `.scss`, `.sass`, `.less`, `.ts`, `.js`). Reminders can arrive after an edit or at session completion, depending on the hook integration. Plain `.ts` and `.js` stay quiet unless the detector finds something. `hook.quiet` silences clean and pending acknowledgements.

With a completion hook that returns findings, the per-edit pass can focus on mechanical problems such as broken images, overflow, contrast, and design-system drift. The completion pass runs the full set on touched UI files and deduplicates earlier findings. Set `hook.perEditRules` to `"all"` in `.impeccable/config.json` to run the full set on every edit.

Every hook is a mechanical pass. The reflexes no scanner catches live in [craft-floor.md](craft-floor.md), which the skill loads before it edits UI, so they apply whether or not a hook is wired. A session with no automatic hook gets one `MANUAL_DETECTOR_REQUIRED` directive from `impeccable context` asking for a single detector run at the end.

This command toggles the hook **per project** by editing `.impeccable/config.json` (the unified Impeccable config; hook runtime settings live under its `hook` key, and shared detector ignores live under `detector`). Per-developer overrides, including the install consent decision (`hook.consent`) the CLI records, live in the gitignored `.impeccable/config.local.json`. Set `hook.enabled: false` to turn the hook off, `hook.quiet: true` to silence the clean/pending acks, or `hook.auditLog` to a file path for an NDJSON log. The legacy `IMPECCABLE_HOOK_DISABLED`, `IMPECCABLE_HOOK_QUIET`, and `IMPECCABLE_HOOK_LOG` env vars are still honored and override these config values when set.

Declare server-side template extensions under **`detector.extensions`** when the project uses Blade, Twig, ERB, or Handlebars files; the hook skips them otherwise because they sit outside the built-in extension list. One entry per extension, `{ "ext": ".blade.php", "engine": "html" }`. `engine` picks the analyzer (`html` for markup templates, `text` for JS/TS/CSS-like files) and defaults to `html`. Match against the end of the filename, so double extensions like `.blade.php` and `.html.erb` work. Config only adds extensions; the built-in list always applies.

Manual `"<skill-base-dir>/scripts/impeccable" detect` scans use the same project filter config by default: `detector.ignoreRules`, `detector.ignoreFiles`, `detector.ignoreValues`, and `detector.designSystem.enabled`. `hook.enabled` only controls automatic hook execution, not manual CLI scans. Use `"<skill-base-dir>/scripts/impeccable" detect --no-config ...` for a raw detector run that ignores project config/context. Use `"<skill-base-dir>/scripts/impeccable" ignores ...` for direct CLI CRUD on the same detector ignores.

## Routing

The first argument is the action. Defaults to `status`.

| Action | What it does |
|---|---|
| `status` | Print current state, shared/local config paths, ignored rules / files / values, env override. |
| `on` | Automatic hook integration is configured separately. Use manual `detect` until the hook is verified. |
| `off` | Set `enabled: false` in `.impeccable/config.json`. |
| `ignore-rule <id>` | Append `<id>` to `detector.ignoreRules`; for `overused-font`, requires `--all-values`. Suppresses the rule across the whole project. |
| `ignore-file <glob>` | Append `<glob>` to `detector.ignoreFiles`. Suppresses **every** rule for matching files. |
| `ignore-value <id> <value> [--shared] [--reason "..."]` | Append a rule/value suppression to shared `.impeccable/config.json`. |
| `ignore-value <id> <value> --local [--reason "..."]` | Append a private rule/value suppression to `.impeccable/config.local.json`. |
| `ignore-value <id> "*" --file <glob> [--file <glob>...]` | Turn one rule off in matching files only, leaving it active everywhere else. Repeat `--file`, or use `--file=<glob>` / `--files=<glob>`. A bare `"*"` with no `--file` is refused: use `ignore-rule <id>` if you really mean project-wide. |
| `reset` | Delete the project config and detector caches, and remove hook entries installed by the engine. Review the scope first. |

## Flow

1. Resolve the action from the user's argument. Default to `status`. For `on`, point to the [upstream setup instructions](https://github.com/pbakaus/impeccable) for the user’s environment and use manual `detect` until a hook is verified. Stop here for `on`.
2. Invoke the admin script and pass the user's output through verbatim:

   ```bash
   "<skill-base-dir>/scripts/impeccable" hooks <action> [args...]
   ```

3. For ignore changes, the default scope is shared `.impeccable/config.json`. Add `--local` only for an explicitly requested private exception.
4. For `status`, explain that the printed state is configuration and use manual `detect` when hook delivery is unverified.

## Triage findings

The hook itself never writes ignore config; every exception goes through `impeccable hooks`. Triage each finding into one of three outcomes:

- **Real design problem**: fix it. Never add an ignore to skip a fix or to push a blocked write through.
- **Confident false positive or sanctioned exception**: persist the narrowest ignore yourself and disclose it in your reply. The bar is evidence you can name: an intentional demo or fixture, documentation of bad design, literal or domain-appropriate motion (a ball that bounces), or a choice the user already confirmed. Put that evidence in `--reason` as `"<who decided: evidence>"`; write "user confirmed" only when the user actually did.
- **Unsure**: leave the finding standing and ask the user in one line. Ask once; a one-line question costs less than the hook re-firing on every later edit.

Self-serve stops at `ignore-value`. `ignore-file` and `ignore-rule` silence too much to add on your own judgment; ask the user first.

Prefer the narrowest exception:

- If the finding line shows an `ignore-value <rule> <value>` pair, pass it to `impeccable hooks ignore-value` with your `--reason`. This writes shared `.impeccable/config.json` by default.
- For value-specific findings such as `overused-font` and `bounce-easing`, use `ignore-value` for the specific value. Do not use `ignore-rule overused-font` for a specific font.
- If the finding has no value-specific command, such as `side-tab`, scope that one rule to the file: `ignore-value <id> "*" --file <path>`. Run `"<skill-base-dir>/scripts/impeccable" detect <path>` first to see what actually fires there.
- Reach for `ignore-file <path>` only when the whole file is out of scope for design review: a fixture, a generated artifact, a deliberate slop demo. It silences every rule for that file permanently, including rules that have not been written yet. A real UI surface with one noisy rule wants the file-scoped value ignore above.
- Use `ignore-rule <id>` only when the user asks to suppress that whole rule across the project. For broad overused-font suppression, use `ignore-rule overused-font --all-values` only when the user asks to ignore overused fonts generally.
- Prefer config ignores (the commands above) by default; they keep suppressions in one reviewable place. Reach for an inline comment only when the waiver must travel with a single file that leaves the repo (a generated/exported standalone document, an emailed HTML file). The supported marker is `impeccable-disable <rule>` (whole file) or `impeccable-disable-line` / `impeccable-disable-next-line` (one line), in any comment syntax, with an optional reason after `:` or `--`. The detector honors it by default; `--no-inline-ignores` or `--no-config` bypasses it.

Example value-specific exception:

```bash
"<skill-base-dir>/scripts/impeccable" hooks ignore-value overused-font Inter --shared --reason "User confirmed Inter is intentional"
```

Example self-served exception, with the evidence named:

```bash
"<skill-base-dir>/scripts/impeccable" hooks ignore-value bounce-easing bounce-ball --shared --reason "Agent: literal ball-bounce animation, bounce easing is the subject"
```

Example whole-rule font exception:

```bash
"<skill-base-dir>/scripts/impeccable" hooks ignore-rule overused-font --all-values --reason "User asked to ignore overused fonts generally"
```

Example one-rule-in-one-file exception, for a file that is still worth reviewing
for everything else:

```bash
"<skill-base-dir>/scripts/impeccable" hooks ignore-value design-system-font-size "*" --file "src/overlay/widget.js" --reason "Injected widget builds its own type scale; DESIGN.md's ramp describes the site"
```

Example whole-file exception, for a file that is out of scope entirely:

```bash
"<skill-base-dir>/scripts/impeccable" hooks ignore-file "src/legacy/Card.tsx"
```

## Constraints

- Never modify `.impeccable/config.json` or `.impeccable/config.local.json` by hand from this command. Always go through `impeccable hooks` so writes stay validated and the file shape stays consistent. One exception: `detector.extensions` has no admin action, so when the user asks to cover a template stack, edit that one field in `.impeccable/config.json` directly and leave the rest of the file untouched.
- Do not edit the launcher or the binary behind `impeccable hook` and `impeccable hook-before-edit` from this flow. Those are skill plumbing.
- The current per-edit hook emits a reminder after the edit. Older pre-edit hooks may block writes. Disabling stops hook reminders.
- Leave registrations, scope, and trust settings to the user’s agent configuration.

## Failure modes

- If `.impeccable/config.json` or `.impeccable/config.local.json` is unreadable or malformed, the hook ignores that file and uses the remaining valid config/defaults. `impeccable hooks status` will show malformed files as ignored.
- If the user asks to "disable the hook" globally, lead with `impeccable hooks off` (persistent for this project; writes `hook.enabled: false` to config). The legacy `IMPECCABLE_HOOK_DISABLED=1` env var also works as a one-shot override that follows the shell.
