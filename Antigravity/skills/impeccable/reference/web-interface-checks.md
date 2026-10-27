# Additional web interaction checks

Read the groups relevant to the requested web review. These checks supplement the existing audit; they do not require a separate audit pass or a broader environment setup.

## Forms and feedback

- Check meaningful `name`, appropriate `type`, `inputmode`, and `autocomplete` values. Preserve paste and password-manager support.
- Labels should activate their controls. Verify pending submission, inline errors, and a useful focus/announcement path when submission fails.
- Native buttons and links already provide keyboard behavior; custom controls need the equivalent behavior without duplicate activation.

## Focus and navigation

- Sticky headers, footers, and overlays must not obscure the focused control. Relevant heading anchors need suitable scroll spacing.
- Navigation should retain browser link behavior, including opening in another tab.
- Where sharing, restoration, or back/forward navigation is required, keep meaningful filters, tabs, or pagination in the URL. Local transient state need not become URL state; sensitive values must stay out of URLs.

## Server-rendered UI

Check server/client consistency for time, locale-dependent output, and initial input state. Resolve the actual mismatch rather than applying blanket hydration-warning suppression.

Report verified findings through the existing file/location/impact format. Distinguish code inspection from behavior actually exercised. Apply local language conventions; the source's English capitalization and stylistic preferences are not universal requirements.

Adapted selectively from [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines/blob/434b7f91364665f2f733b310ec54809bf8f37937/command.md), inspected 2026-10-25.
