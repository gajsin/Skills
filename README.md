# Agent Skills

Reusable skills for coding agents: engineering discipline,
debugging, review, interviews, UI design, animation, writing, and model
qualification. Shared principles are adapted to each host's tools, invocation,
and capabilities. Host-specific upstream builds may also differ.

| Host | Release archive | Invoke |
|---|---|---|
| Codex | [gajsin-skills-codex.zip](https://github.com/gajsin/Skills/releases/download/skills/gajsin-skills-codex.zip) | `$name` |
| Claude Code | [gajsin-skills-claude.zip](https://github.com/gajsin/Skills/releases/download/skills/gajsin-skills-claude.zip) | `/name` |
| Antigravity | [gajsin-skills-antigravity.zip](https://github.com/gajsin/Skills/releases/download/skills/gajsin-skills-antigravity.zip) | `/name` |

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
| `editor` | Prepare articles, posts, and promotional copy for publication, or edit drafts. One invocation selects the workflow. |
| `impeccable` | Design, critique, audit, and polish user interfaces (by [pbakaus/impeccable](https://github.com/pbakaus/impeccable)). |
| `gsap` | Implement GSAP website animation; read React lifecycle and ScrollTrigger guidance only when relevant. |
| `logo-interview` | Find a logo direction through an interview, a moodboard, and SVG studies. |
| `visual-explainer` | Author SVG illustrations and diagrams directly in code, without image-generation services; use the bundled monochrome design and animate when requested. |
| `model-provider-qualification` | Qualify an LLM model and provider route with cheap canaries before a paid pipeline run. |

How the close neighbours differ and how to combine skills: [GUIDE.md](GUIDE.md).

## Repository layout

```text
skills/                complete skills for direct installation
platforms/codex/       Codex-specific files and invocation policies
platforms/claude/      Claude Code-specific files and Impeccable helper agents
AGENTS.md              shared working principles (Russian)
GUIDE.md               choosing and combining skills
catalog.json           public Russian skill cards and their display order
scripts/               builder for release archives
```

## Install

### Install one skill from GitHub

Give your agent a link to a complete skill directory in [`skills/`](skills):

> Install Humanizer from https://github.com/gajsin/Skills/tree/main/skills/humanizer
> into my personal skills folder. Keep its license, references, and helper files.

The shared directories contain the Antigravity edition and are ready to copy.
Use the Codex or Claude Code archive for that host's manual-only invocation
settings and native Impeccable roles, including when installing just one skill.
The pack builder applies the files in `platforms/` to `skills/`.

### Copy skill directories manually

Unpack the archive for your host, then copy the desired skills to the destination below.
Keep each directory intact: it carries its license, references, and helper scripts.
Copying updates matching files; it does not remove obsolete files from an existing
installation. Restart the agent if the changes do not appear.

| Host | Copy `skills/<skill-name>/` into |
|---|---|
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Antigravity App/IDE and CLI | `~/.gemini/config/skills/` |

Antigravity CLI also reads `~/.gemini/antigravity-cli/skills/` and
`~/.gemini/skills/`. Copies there take priority over the shared directory.
CLI 1.5.16 and later also load `~/.agents/skills/`, with same-named skills
under `~/.gemini/` taking precedence. Run `/skills reload` after updating skills
in an open CLI session. See [skill discovery](https://antigravity.google/docs/customization-discovery/)
and the [CLI changelog](https://antigravity.google/docs/changelog?tab=hub#v1.5.16).

### Install Impeccable helper roles

| Host | Copy | Into |
|---|---|---|
| Codex | `skills/impeccable/agents/*.toml` from the Codex archive | `~/.codex/agents/` or the project's `.codex/agents/` |
| Claude Code | `agents/*.md` from the Claude Code archive | `~/.claude/agents/` or the project's `.claude/agents/` |

Use one registration per role. The Codex role names use hyphens. Keep
`agents/openai.yaml` inside the skill folder. Antigravity Impeccable can delegate
from bundled role instructions on its own.

The Claude Code paths above are for local sessions. SSH sessions use the remote
home folder. Cloud sessions can load skills from the checked-out project.
[Desktop skills](https://code.claude.com/docs/en/desktop#use-skills)

`gsap` replaces `gsap-react` and `gsap-scrolltrigger`. Install the complete new
`gsap/` directory, verify it is available, then remove those two old directories
from your personal skills location. Copying a new pack alone does not remove them.

### Install the Claude Code pack from an extracted archive

```bash
mkdir -p ~/.claude/skills ~/.claude/agents
cp -r skills/* ~/.claude/skills/
cp agents/*.md ~/.claude/agents/
```

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills", "$env:USERPROFILE\.claude\agents" | Out-Null
Copy-Item -Recurse -Force "skills\*" "$env:USERPROFILE\.claude\skills"
Copy-Item -Force "agents\*.md" "$env:USERPROFILE\.claude\agents"
```

### Optional personal rules

To use the repository's [working principles](AGENTS.md) across your projects,
copy the contents of `AGENTS.md` to the personal rules file for your host.
Review your existing rules before replacing them.

| Host | Personal rules file |
|---|---|
| Codex | `~/.codex/AGENTS.md` |
| Antigravity | `~/.gemini/config/GEMINI.md` |
| Claude Code | `~/.claude/CLAUDE.md` |

Impeccable downloads its official engine, with checksum verification, on first use.

## Release archives

### Public cards on gajsin.tech

`catalog.json` is the single source for each skill's Russian card and the order
of cards on the website. It is keyed by the skill directory name. Every entry
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
the desired position, the shared skill and any host-specific files, license, and
provenance. When removing or renaming a skill, remove or rename its card as well.
Keep statements factual:
do not invent capabilities, guarantees, or permissions. Match shared cards to the
behavior of the host editions; mention material differences when they exist.

Before pushing, run:

```sh
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/publish_manifest.py --output dist --download-base https://github.com/gajsin/Skills/releases/download/skills
```

Check the generated `dist/skills.json`: names, order, categories, descriptions,
results, boundaries, and all three packs. The builder checks the skill names in
all three packs against the catalog and rejects missing fields or empty values
before creating archives. Do not commit
`dist/`. Use a clear commit title and body describing the actual user-facing
change: the website's journal displays that text.

Pushing to `main` runs `.github/workflows/publish.yml`. It publishes the packs,
cards and up to 20 journal entries in the `skills` release. The first release
with a journal reads Git history. Later releases keep existing entries and add
the relevant commits since the previous release, including catalogue changes.
After publication, the workflow refreshes the portfolio cache using the
`SKILLS_REVALIDATE_SECRET` repository secret. Set the same server-only secret
on the portfolio after deploying its refresh endpoint. Wait for the successful
workflow and verify the released manifest and archives.

Build a source-only archive per host with Python 3 (standard library only):

```sh
python scripts/package_skills.py --platform codex --output dist/codex-skills.zip
python scripts/package_skills.py --platform claude --output dist/claude-code-skills.zip
python scripts/package_skills.py --platform antigravity --output dist/antigravity-skills.zip
```

Archives provide optional bulk downloads for the website and offline installation.
Each holds the skills, installation and role setup instructions, the skill guide,
and a license table. Claude Code also includes its helper roles in `agents/`.
The archives exclude the repository's `AGENTS.md` and Git history. Individual
skills can also be installed directly from the public repository.

## Licenses

| Skills | License | Origin |
|---|---|---|
| architecture-first, model-provider-qualification, logo-interview, visual-explainer | MIT | Original, © gajsin |
| diagnosing-bugs, spec-review, codebase-design, grilling, retro | MIT | Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) |
| ponytail | MIT | Adapted from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |
| humanizer | MIT | Adapted from [blader/humanizer](https://github.com/blader/humanizer) |
| editor | CC BY 4.0 | Adapted from [N1arko/redaktura-skills](https://github.com/N1arko/redaktura-skills), by Lyudmila Sarycheva and Nikita Arkhipov |
| gsap | MIT | Consolidated from [greensock/gsap-skills](https://github.com/greensock/gsap-skills); original license retained |
| caveman | Apache-2.0, with a retained MIT notice | Adapted from [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) |
| impeccable | Apache-2.0; embedded references keep their MIT notices | Adapted from [pbakaus/impeccable](https://github.com/pbakaus/impeccable) and credited sources |

Every skill directory contains its license and notices; keep them when you copy or
redistribute a skill. `scripts/` is MIT. Linked reference images and articles keep
their own rights.

Visual Explainer bundles Martian Mono separately under OFL-1.1; keep its
[font notice](skills/visual-explainer/NOTICE.md) and `assets/fonts/OFL.txt`.
Its instructions remain MIT. St Marie Thin is not distributed in the pack.
