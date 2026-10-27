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
| `gsap-scrolltrigger` | Implement scroll-linked website animation with GSAP ScrollTrigger. |
| `gsap-react` | Set up GSAP in React or Next.js with scoped animations and cleanup. |
| `logo-interview` | Find a logo direction through an interview, a moodboard, and SVG studies. |
| `model-provider-qualification` | Qualify an LLM model and provider route with cheap canaries before a paid pipeline run. |

How the close neighbours differ and how to combine skills: [GUIDE.md](GUIDE.md).

## Repository layout

```text
Codex/skills/          skills for Codex, with agents/openai.yaml invocation policies
Claude Code/skills/    skills for Claude Code
Claude Code/agents/    Impeccable helper agents for Claude Code
Antigravity/skills/    skills for Antigravity
Codex/AGENTS.md, Antigravity/GEMINI.md, Claude Code/CLAUDE.md
                       the author's own always-on rules (Russian), optional
Claude Code/PROJECT-RULES.md
                       the author's stack preferences for per-project rules
GUIDE.md               choosing and combining skills
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

The author's global rules files are not required by any skill. Read them before
use: copying one replaces your own `AGENTS.md`, `GEMINI.md`, or `CLAUDE.md`.

Impeccable downloads its official engine, with checksum verification, on first use.

## Release archives

Build a source-only archive per host with Python 3 (standard library only):

```sh
python scripts/package_skills.py --platform codex --output dist/codex-skills.zip
python scripts/package_skills.py --platform claude --output dist/claude-code-skills.zip
python scripts/package_skills.py --platform antigravity --output dist/antigravity-skills.zip
```

Archives provide optional bulk downloads for the website and offline installation.
Each holds the skills (and, for Claude Code, the agents), a README with installation,
the skill guide, and a license table. The author's global rules and Git history are
excluded. Individual skills can also be installed directly from the public repository.

## Licenses

| Skills | License | Origin |
|---|---|---|
| architecture-first, model-provider-qualification, logo-interview | MIT | Original, © gajsin |
| diagnosing-bugs, spec-review, codebase-design, grilling, retro | MIT | Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) |
| ponytail | MIT | Adapted from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |
| humanizer | MIT | Adapted from [blader/humanizer](https://github.com/blader/humanizer) |
| gsap-react, gsap-scrolltrigger | MIT | Adapted from [greensock/gsap-skills](https://github.com/greensock/gsap-skills) |
| caveman | Apache-2.0, with a retained MIT notice | Adapted from [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) |
| impeccable | Apache-2.0; embedded references keep their MIT notices | Adapted from [pbakaus/impeccable](https://github.com/pbakaus/impeccable) and credited sources |

Every skill directory contains its license and notices; keep them when you copy or
redistribute a skill. `scripts/` is MIT. Linked reference images and articles keep
their own rights.
