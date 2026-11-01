# Publishing skill updates

- When adding or improving skills, use focused commits with a clear Russian
  subject and a short description for the portfolio's update journal: affected
  skills, concrete changes, and their purpose. Describe completed changes; distinguish
  verification from untested behavior and avoid claims of guaranteed results.
- For future updates, preserve published history with ordinary commits and pushes.
  Do not amend, squash, or force-push published history unless the user explicitly
  asks to rewrite it. Keep unrelated changes outside the skill update.
- Keep `catalog.json` synchronized with skill additions, removals, renames, and
  behavior changes: review `group`, `use`, `result`, and `edits` in the same commit.
  The site's description and license come from `Claude Code/skills/<name>/SKILL.md`.
  Run the checks in README's "Public cards on gajsin.tech" section before pushing.
- Validate the affected host editions and preserve their invocation policies.
  Confirm that the publication workflow succeeds and the `skills` release archives
  and manifest match the published commit. The site refreshes its cache without a
  portfolio deployment; do not edit the portfolio merely to publish a skill update.
