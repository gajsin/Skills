# SPDX-License-Identifier: MIT
# Copyright (c) 2026 gajsin
"""Build reviewed source-only download bundles with per-skill licenses."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import zipfile

PLATFORMS = {'codex': 'Codex', 'antigravity': 'Antigravity', 'claude': 'Claude Code'}
LOCATIONS = {
    'codex': '~/.agents/skills',
    'antigravity': '~/.gemini/config/skills',
    'claude': '~/.claude/skills',
}
POLICIES = {
    'codex': 'Codex invocation policies are included.',
    'antigravity': ("Antigravity's manual-only preference is expressed in the descriptions;\n"
                    'it is not a technical enforcement guarantee. The location above is for\n'
                    'App/IDE; CLI users copy skills to `~/.gemini/antigravity-cli/skills`.'),
    'claude': ('Every skill sets `disable-model-invocation: true`. Copy the files in\n'
               '`agents/` to `~/.claude/agents` for the Impeccable helper agents.'),
}
ORIGINS = {
    **{name: 'https://github.com/mattpocock/skills/tree/5beb35b' for name in
       ['diagnosing-bugs', 'spec-review', 'codebase-design', 'grilling', 'retro']},
    'ponytail': 'https://github.com/DietrichGebert/ponytail/tree/09c434a',
    'caveman': 'https://github.com/juliusbrussee/caveman/tree/9b68f7ed12b05e7efaff18e65c5a3fc2849fd0a4',
    'humanizer': 'https://github.com/blader/humanizer/tree/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8',
    'impeccable': 'https://github.com/pbakaus/impeccable/tree/936867543ac2576920d663cc9803597f6044f3ac',
    **{name: 'https://github.com/greensock/gsap-skills/tree/aed9cfd3277740755f6bfc1155c7aa645403b760'
       for name in ['gsap-react', 'gsap-scrolltrigger']},
    **{name: 'https://github.com/gajsin/skills' for name in
       ['architecture-first', 'model-provider-qualification', 'logo-interview']},
}
SKIP_DIRS = {'.git', '.cache', '__pycache__', 'node_modules', '.venv'}


def build_bundle(repo_root, platform, output):
    root = (repo_root / PLATFORMS[platform] / 'skills').resolve()
    if not root.is_dir():
        raise ValueError(f'Missing skill source directory: {root}')
    output = output.resolve()
    if root == output or root in output.parents:
        raise ValueError('The archive must be outside the skill source directory.')
    skills = sorted(p for p in root.iterdir() if p.is_dir() and (p / 'SKILL.md').is_file())
    if not skills:
        raise ValueError('No skills found.')
    files = []
    rows = []
    for skill in skills:
        if skill.name not in ORIGINS:
            raise ValueError(f'Add provenance for the new skill before packaging: {skill.name}')
        if not (skill / 'LICENSE').is_file():
            raise ValueError(f'Missing LICENSE: {skill.name}')
        manifest = (skill / 'SKILL.md').read_text(encoding='utf-8')
        license_match = re.search(r'^license:\s*(.+)$', manifest, re.M)
        if not license_match:
            raise ValueError(f'Missing license declaration: {skill.name}')
        license_name = license_match.group(1).strip().strip('\"\'')
        rows.append(f'| [{skill.name}](skills/{skill.name}/SKILL.md) | [{license_name}](skills/{skill.name}/LICENSE) | [Source]({ORIGINS[skill.name]}) |')
        for path in sorted(skill.rglob('*')):
            rel = path.relative_to(root)
            if any(part in SKIP_DIRS for part in rel.parts) or path.suffix in {'.pyc', '.pyo'}:
                continue
            if path.is_symlink():
                raise ValueError(f'Resolve symlinks before packaging: {rel}')
            if not path.is_file():
                continue
            if root not in path.resolve().parents or any(part.startswith('.env') for part in rel.parts):
                raise ValueError(f'Unexpected source path: {rel}')
            if path.suffix.lower() in {'.exe', '.dll', '.so', '.dylib'}:
                raise ValueError(f'Runtime binaries do not belong in this source bundle: {rel}')
            files.append(('skills/' + rel.as_posix(), path.read_bytes()))
    agents = root.parent / 'agents'
    if agents.is_dir():
        for path in sorted(agents.glob('*.md')):
            files.append(('agents/' + path.name, path.read_bytes()))
    marker = '$' if platform == 'codex' else '/'
    location = LOCATIONS[platform]
    # GUIDE.md is the single source; its headings move one level down inside the README.
    guide = ''.join('#' + line if line.startswith('#') else line
                    for line in (repo_root / 'GUIDE.md').read_text(encoding='utf-8').splitlines(True))
    readme = f'''# {PLATFORMS[platform]} Skill Pack

Reusable English instructions; agents should respond in the user's language.
Copy the individual directories inside `skills/` to `{location}`. Keep each
directory intact, including its LICENSE, notices, references, and helpers.
Create the destination directory if needed. Copying updates matching files; it
does not remove obsolete files from an existing installation.

Invoke a skill explicitly, for example `{marker}grilling` or `{marker}logo-interview`.
{POLICIES[platform]}

These are original skills and attributed adaptations, not a claim that every skill
was written from scratch. The root LICENSE covers the pack-owned README and
packaging material. Each skill retains its own license; this bundle does not
relicense third-party work. Linked external images and material retain their rights.
Impeccable may download its official engine with checksum verification on first use.

Personal global instructions, internal reports, caches, and Git history are excluded.
No Figma or Pinterest account is required. Visual tools depend on the active host.
Skills guide behavior; they do not guarantee correctness or production readiness.

''' + guide + '''
## Licenses and origins

| Skill | License | Origin |
|---|---|---|
''' + '\n'.join(rows) + '\n'
    files.append(('README.md', readme.encode('utf-8')))
    files.append(('LICENSE', (repo_root / 'scripts/LICENSE').read_bytes()))
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 25, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if data.startswith(b'#!') else 0o100644) << 16
            archive.writestr(info, data)
    return {'platform': platform, 'skills': len(skills), 'files': len(files),
            'sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'bytes': output.stat().st_size}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--platform', choices=PLATFORMS, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = build_bundle(Path(__file__).resolve().parents[1], args.platform, args.output)
    print(json.dumps(result))
