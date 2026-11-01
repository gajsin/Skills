# Agent Skills

Reusable skills for coding agents: engineering discipline,
debugging, review, interviews, UI design, animation, writing, and model
qualification. Shared principles are adapted to each host's tools, invocation,
and capabilities. Host-specific upstream builds may also differ.

| Host | Folder | Invoke |
|---|---|---|
| Codex | [`Codex/`](Codex) | `$name` |
| Claude Code | [`Claude Code/`](Claude%20Code) | `/name` |
| Antigravity | [`Antigravity/`](Antigravity) | `/name` |

## Skills

| Skill | What it is for |
|---|---|
| `architecture-first` | Make a substantial change to a working system: trace the real path, choose the smallest supported design, implement only what was asked, review before release. |
| `ponytail` | Session mode: solve each coding task with the smallest complete change, no speculative code. |
| `codebase-design` | Decide module interfaces, seams, and testability; `audit` reports evidence-backed architecture improvements. |
| `spec-review` | Review changes or audit an existing project on standards and requirements, with scoped automated code-quality evidence. |
| `diagnosing-bugs` | Find the cause of a hard bug or performance regression through a verified reproduction loop, then fix it. |
| `grilling` | Interview the user to settle requirements and design decisions; write a spec or task plan on request. |
| `retro` | Review an agent session and propose the smallest evidence-backed corrections. |
| `caveman` | Session mode: short, dry, grammatical replies without losing facts. |
| `humanizer` | Write or edit natural prose and concise session summaries from the available context, preserving facts and the intended voice. |
| `impeccable` | Design, critique, audit, and polish user interfaces (by [pbakaus/impeccable](https://github.com/pbakaus/impeccable)). |
| `gsap` | Implement GSAP website animation; read React lifecycle and ScrollTrigger guidance only when relevant. |
| `logo-interview` | Find a logo direction through an interview, a moodboard, and SVG studies. |
| `visual-explainer` | Author SVG illustrations and diagrams directly in code, without image-generation services; use the bundled monochrome design and animate when requested. |
| `model-provider-qualification` | Qualify an LLM model and provider route with cheap canaries before a paid pipeline run. |

How the close neighbours differ and how to combine skills: [GUIDE.md](GUIDE.md).

## Repository layout

```text
Codex/skills/          skills for Codex, with agents/openai.yaml invocation policies
Claude Code/skills/    skills for Claude Code
Claude Code/agents/    Impeccable helper agents for Claude Code
Antigravity/skills/    skills for Antigravity
Codex/AGENTS.md, Antigravity/GEMINI.md, Claude Code/CLAUDE.md
                       optional reusable agent-rule examples
Claude Code/PROJECT-RULES.md
                       optional examples of project-specific requirements
GUIDE.md               choosing and combining skills
catalog.json           public Russian skill cards and their display order
scripts/               builder for release archives
```

## Install

### Install one skill from GitHub

Give your agent the link to the skill directory for its host. For example, in Codex:

> Install Humanizer from https://github.com/gajsin/Skills/tree/main/Codex/skills/humanizer
> into my personal skills folder. Keep its license, references, and helper files.

For another host, choose the corresponding directory under `Claude Code/skills/`
or `Antigravity/skills/`. Install the complete skill directory, not just SKILL.md.
Release archives are optional; a GitHub directory link is enough to locate a skill.

### Copy skill directories manually

Create the destination directory, then copy the desired skills for your host.
Keep each directory intact: it carries its license, references, and helper scripts.
Copying updates matching files; it does not remove obsolete files from an existing
installation. Restart the agent if the changes do not appear.

| Host | Copy | Into |
|---|---|---|
| Codex | `Codex/skills/<skill-name>/` | `~/.agents/skills/` |
| Claude Code | `Claude Code/skills/<skill-name>/` | `~/.claude/skills/` |
| Antigravity App/IDE | `Antigravity/skills/<skill-name>/` | `~/.gemini/config/skills/` |

For Antigravity CLI, use `~/.gemini/antigravity-cli/skills/` instead. Existing
working installations do not need to be moved merely to follow this table.
When installing Impeccable for Claude Code, also copy `Claude Code/agents/*`
into `~/.claude/agents/`.

`gsap` replaces `gsap-react` and `gsap-scrolltrigger`. Install the complete new
`gsap/` directory, verify it is available, then remove those two old directories
from your personal skills location. Copying a new pack alone does not remove them.

The following examples install the full Claude Code pack from a repository checkout:

```bash
mkdir -p ~/.claude/skills ~/.claude/agents
cp -r "Claude Code/skills/"* ~/.claude/skills/
cp "Claude Code/agents/"* ~/.claude/agents/
```

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills", "$env:USERPROFILE\.claude\agents" | Out-Null
Copy-Item -Recurse -Force "Claude Code\skills\*" "$env:USERPROFILE\.claude\skills"
Copy-Item -Force "Claude Code\agents\*" "$env:USERPROFILE\.claude\agents"
```

The optional agent-rule examples are not required by any skill. Review and adapt
them before use; copying one replaces your existing `AGENTS.md`, `GEMINI.md`, or
`CLAUDE.md`.

Impeccable downloads its official engine, with checksum verification, on first use.

## Release archives

### Catalog metadata

`catalog.json` is the single source for each skill's Russian card and its display
order in catalog consumers. It is keyed by the skill directory name. Every entry
must contain four non-empty text fields:

| Field | Meaning |
|---|---|
| `group` | Category, for example `Дизайн и анимация` |
| `use` | When to use the skill; the short summary beside its name |
| `result` | What the user receives |
| `edits` | Boundaries: what it changes, preserves, or requires a separate request |

The English `description` and `license` come from the Claude Code edition's
`SKILL.md` frontmatter; provenance comes from `ORIGINS` in
`scripts/package_skills.py`. Do not duplicate these fields in `catalog.json`.

When changing a skill, check its card against the actual instructions and update
the relevant fields in the same commit. For a new skill, add a complete card in
the desired position, the host editions, license, and provenance. When removing
or renaming a skill, remove or rename its card as well. Keep statements factual:
do not invent capabilities, guarantees, or permissions. Match shared cards to the
behavior of the host editions; mention material differences when they exist.

Before pushing, run:

```sh
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/publish_manifest.py --output dist --download-base https://github.com/gajsin/Skills/releases/download/skills
```

Check the generated `dist/skills.json`: names, order, categories, descriptions,
results, boundaries, and all three packs. The builder rejects missing or obsolete
cards, missing fields, and empty values before creating archives. Do not commit
`dist/`. Use a clear commit title and body describing the actual user-facing
change so downstream changelogs can use that text.

Pushing to `main` runs `.github/workflows/publish.yml`, which publishes the packs
and complete cards in the `skills` release. Wait for the successful workflow and
verify the released manifest and archives. Consumers may cache the manifest;
their refresh policy is independent of the release build.

Build a source-only archive per host with Python 3 (standard library only):

```sh
python scripts/package_skills.py --platform codex --output dist/codex-skills.zip
python scripts/package_skills.py --platform claude --output dist/claude-code-skills.zip
python scripts/package_skills.py --platform antigravity --output dist/antigravity-skills.zip
```

Archives provide optional bulk downloads and offline installation.
Each holds the skills (and, for Claude Code, the agents), a README with installation,
the skill guide, and a license table. Optional global-rule examples and Git history are
excluded. Individual skills can also be installed directly from the public repository.

## Licenses

| Skills | License | Origin |
|---|---|---|
| architecture-first, model-provider-qualification, logo-interview, visual-explainer | MIT | Original, © gajsin |
| diagnosing-bugs, spec-review, codebase-design, grilling, retro | MIT | Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) |
| ponytail | MIT | Adapted from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |
| humanizer | MIT | Adapted from [blader/humanizer](https://github.com/blader/humanizer) |
| gsap | MIT | Consolidated from [greensock/gsap-skills](https://github.com/greensock/gsap-skills); original license retained |
| caveman | Apache-2.0, with a retained MIT notice | Adapted from [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) |
| impeccable | Apache-2.0; embedded references keep their MIT notices | Adapted from [pbakaus/impeccable](https://github.com/pbakaus/impeccable) and credited sources |

Every skill directory contains its license and notices; keep them when you copy or
redistribute a skill. `scripts/` is MIT. Linked reference images and articles keep
their own rights.

Visual Explainer bundles Martian Mono separately under OFL-1.1; keep its
[font notice](Codex/skills/visual-explainer/NOTICE.md) and `assets/fonts/OFL.txt`.
Its instructions remain MIT. St Marie Thin is not distributed in the pack.
