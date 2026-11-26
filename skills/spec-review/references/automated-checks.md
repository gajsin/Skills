# Automated code-quality evidence

Use these checks within the requested review scope. They find evidence; they do
not replace the Standards or Spec assessment, authorize fixes, or prove that an
application works. For a whole-project audit, inspect the project and representative
flows as well as the reports. For a diff, keep findings tied to changed behavior
and directly affected callers; broaden the scanned comparison set when needed to
find a duplicate outside the diff, and state that scope.

## One invocation, explicit outcomes

The user need not name the tools. For applicable source code, run the shared
inspector and examine its evidence. Always account for Crapper, Dryer, and Mutator
in the final report: performed with result and limits, not applicable with reason,
or not performed with reason. `scan_only` means mutation tests were not run.
Never convert absence, a parser error, missing coverage, zero selected mutations,
or a successful process exit into a quality pass. Documentation-only work needs
no tool setup; state that these checks are not applicable.

## Runtime setup

Resolve commands from the directory containing this SKILL.md, not the project.
Use an actual Python 3.11+ interpreter; a Windows Store alias is not an interpreter.

```text
python <skill-dir>/scripts/quality_tools.py status
python <skill-dir>/scripts/quality_tools.py setup
```

Setup downloads pinned upstream 0BSD sources and installs their dependencies in a
dedicated user cache, shared by the host editions. A source-checked compatibility
patch adds native Windows execution; its hash is part of the cache identity. `SPEC_REVIEW_TOOLS_HOME` can
select another cache location. Keep the skill directory intact, including its
`patches/` files. Setup does not install project dependencies or alter
package manifests, lockfiles, global instructions, hooks, or system settings.
Follow host network/write permissions. If setup is unavailable or prohibited by
an explicit no-write request, report the missing checks; do not silently install
elsewhere or weaken the review. Do not run the upstream bootstrap shell launchers
or automatic coverage installers against the reviewed project.

## Read-only analysis

For a full project, select `--all`. For a change review, pass existing explicit
file paths from the pinned diff and relevant untracked files; paths are not
substring filters. Source selection excludes dependencies, generated/test
directories, test files, and unsupported languages; inspect the exclusions and
cover relevant tests and unsupported code in the manual review.

```text
python <skill-dir>/scripts/quality_tools.py inspect --root <project> --all --output <outside-project>/quality.json
python <skill-dir>/scripts/quality_tools.py inspect --root <project> --files src/example.py src/other.py --output <outside-project>/quality.json
```

The helper calls the pinned tools' own analysis functions, writes only the named
report outside the project, and verifies selected sources remain unchanged. It
does not create the upstream `.metrics` reports or run tests as a side effect.
Parsers may access their pinned grammar manifest and download grammars into their
user cache. Respect network permissions and disclose an unavailable parser.
Detected syntax/parser errors make the analysis incomplete; these metrics do not
replace the project's syntax/type checks.

- **Crapper:** complexity and CRAP calculation. Without matching current coverage,
  report complexity only; coverage and CRAP remain N/A. Use `--existing-coverage
  --coverage-evidence "<command/CI run and reviewed revision>"` only after verifying
  that the existing reports match the reviewed source. A timestamp alone is not
  provenance. Missing file/function coverage remains unknown, not measured 0%.
  A score is a signal to inspect the function, not an instruction to split it.
- **Dryer:** candidate structural duplicates. Check domain meaning and shared
  responsibility before recommending extraction. Similar shape does not establish
  one business rule. Parser warnings mean incomplete analysis.
- **Mutator:** real upstream mutation-site discovery, with actual mutation tests
  explicitly marked not run. Use it to select testable, consequential changed
  logic. Site discovery is not a test-strength verdict.

## Actual mutation testing

Run when the reviewed behavior and risk justify it and a suitable test suite is
available. Ordinary prose edits do not need it. Inspect the test command before
execution; a review does not authorize production writes, paid calls, dependency
installation, or shared-resource cleanup.

The supplied runtime supports native Windows and the upstream POSIX execution.
Windows workers use independent regular-file copies, including full local
dependency payloads, and Windows Job Objects control test-process lifetimes. No WSL,
Developer Mode, administrator rights, or additional Python dependency is required
by this adaptation. POSIX workers retain the upstream overlay behavior.

Use an independent project snapshot containing the reviewed working files,
including relevant untracked changes. Do not run mutation execution against the
original tree: the tool can restore old backup files, and tests can write through
worker links. Verify snapshot files are independent copies. Keep test/build
artifacts there, and preserve the original project and its dependencies.

Use the real project's interpreter and configured test command, not Mutator's
interpreter by accident. Tests and module imports must follow the worker copy,
not an absolute original source path or an editable install. Verify module origins
for alias/workspace imports. Windows checks every unchanged worker before applying
mutations; a failed worker baseline aborts without scoring those failures as killed.

```text
python <skill-dir>/scripts/quality_tools.py mutate --snapshot <independent-snapshot> --files src/example.py --test-command "<verified-project-test-command>"
```

The separate command requires existing explicit source files and a verified test
command. It rejects Git metadata and old backups. On Windows it checks included
snapshot inputs and existing output paths for reparse points and hard links before the first test process;
prepare a fresh snapshot from independent copies rather than bypassing that check.
Installed runtimes and other external dependencies must already be suitable for
the project. Copying workers is not an operating-system security sandbox.

The test-command string uses the platform shell: `cmd.exe` on Windows, not
PowerShell. Quote paths for that shell. The runner can discover Windows project
interpreters under `.venv/Scripts/python.exe` or `venv/Scripts/python.exe`, but
confirm the actual command and environment instead of assuming the tool's Python
contains the project's dependencies.

This command reruns selected mutants and disables coverage-based filtering; it
does not claim coverage. The default is one worker. `--max-workers` can raise the
cap when justified. Windows copies may cost disk space/time for large dependency
trees, so keep execution scoped to the risk. Windows worker copies use unique
directories under the system temporary directory to avoid extending deep project
paths. Normal filesystem and project-tool path limits still apply; use a short
local snapshot path. Windows baseline tests have a
300-second limit; a verified longer suite can set `MUTATOR_BASELINE_TIMEOUT` to a
positive number of seconds. Mutation timeouts retain the upstream baseline-based
calculation. Do not turn a small review into a full test campaign.

Per-mutation Windows diagnostics retain command, working directory, exit code,
timeout and captured output under `target/mutator-diagnostics` inside the snapshot.
Keep those artifacts local when they contain private project output. Inspect them
when interpreting killed mutants; an execution failure is not a quality pass.

Require positive executed counts. Distinguish surviving, equivalent, uncovered,
invalid/uncompilable, and infrastructure-failed cases. The upstream tool classifies
any failing worker, including import/build failures and timeouts, as killed and
does not retain worker failure output. Its raw killed count is therefore an
upstream classification, not proof of assertion-only detection. Confirm material
findings with focused tests and retained diagnostics; disclose unresolved
classification limits. Never report unconditional mutation quality from its exit
code or score alone. If reliable execution is unavailable, record that limit and
continue the remaining review honestly.

## Sources

Pinned implementations and their own 0BSD licenses:
[Crapper](https://github.com/unclebob/crapper/tree/6fd92c4c9bcc56efb64a2f8743d5a2993bcfd42d),
[Dryer](https://github.com/unclebob/dryer/tree/66ff6d21a42c04afcad89c78a80066176d1294b0),
[Mutator](https://github.com/unclebob/mutator/tree/a5a0cb803b66e0cdb8bf471b3b08af701d424a41).
Their sources and dependencies are fetched into the tool cache, not redistributed
as part of this skill. The included `patches/mutator-windows.patch` modifies
platform integration without replacing mutation discovery or scoring. Its source
is based on the pinned 0BSD upstream. `quality_tools.py` and `patches/windows.py`
are the pack's MIT-licensed integration. Python and Node execution regressions are
maintained in the repository; a passing fixture does not qualify every project or
platform-specific test suite.
