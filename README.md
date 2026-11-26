# Agent Skills

Reusable skills for coding agents: engineering discipline,
debugging, review, interviews, UI design, animation, writing, and model
qualification. Use the same skill directories with any agent that supports
`SKILL.md`. Configure invocation and tools in your own agent.

[Download all skills](https://github.com/gajsin/Skills/releases/download/skills/gajsin-skills.zip)

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
AGENTS.md              shared working principles (Russian)
GUIDE.md               choosing and combining skills
catalog.json           public Russian skill cards and their display order
scripts/               release builder
```

## Install

### Install one skill from GitHub

Give your agent a link to a complete skill directory in [`skills/`](skills):

> Install Humanizer from https://github.com/gajsin/Skills/tree/main/skills/humanizer
> into my personal skills folder. Keep its license, references, and helper files.

### Copy skill directories manually

Unpack the archive, then copy the desired skills to the destination below.
Keep each directory intact: it carries its license, references, and helper scripts.
Copying updates matching files; it does not remove obsolete files from an existing
installation. Restart the agent if the changes do not appear.

| Host | Copy `skills/<skill-name>/` into | Invoke |
|---|---|---|
| Codex | `~/.agents/skills/` | `$name` |
| Claude Code | `~/.claude/skills/` | `/name` |
| Antigravity App/IDE and CLI | `~/.gemini/config/skills/` | `/name` |

Antigravity CLI also reads `~/.gemini/antigravity-cli/skills/` and
`~/.gemini/skills/`. Copies there take priority over the shared directory.
CLI 1.5.16 and later also load `~/.agents/skills/`, with same-named skills
under `~/.gemini/` taking precedence. Run `/skills reload` after updating skills
in an open CLI session. See [skill discovery](https://antigravity.google/docs/customization-discovery/)
and the [CLI changelog](https://antigravity.google/docs/changelog?tab=hub#v1.5.16).

The Claude Code paths above are for local sessions. SSH sessions use the remote
home folder. Cloud sessions can load skills from the checked-out project.
[Desktop skills](https://code.claude.com/docs/en/desktop#use-skills)

`gsap` replaces `gsap-react` and `gsap-scrolltrigger`. Install the complete new
`gsap/` directory, verify it is available, then remove those two old directories
from your personal skills location. Copying a new pack alone does not remove them.

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

## Release archive

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

The English `description` and `license` come from the shared skill's
`SKILL.md` frontmatter. Provenance comes from `ORIGINS` in
`scripts/package_skills.py`. Do not duplicate these fields in `catalog.json`.

When changing a skill, check its card against the actual instructions and update
the relevant fields in the same commit. For a new skill, add a complete card in
the desired position, the skill, its license, and its provenance. When removing
or renaming a skill, update the card to match.

Before pushing, run:

```sh
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/publish_manifest.py --output dist --download-base https://github.com/gajsin/Skills/releases/download/skills
```

Check the generated `dist/skills.json` for card order, descriptions, and the
download link. The builder checks names against the catalog and rejects missing
or empty fields. Keep generated files in `dist/`.

Pushing to `main` runs `.github/workflows/publish.yml`. It publishes the archive,
cards and up to 20 journal entries in the `skills` release. The first release
with a journal reads Git history. Later releases keep existing entries and add
the relevant commits since the previous release, including catalogue changes.
Verify the released manifest and archive after the workflow succeeds.

Build the source archive with Python 3 (standard library only):

```sh
python scripts/package_skills.py --output dist/gajsin-skills.zip
```

The archive contains the skills, installation instructions, the skill guide,
and a license table. Individual skills are also available directly from the
repository.

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
