# SPDX-License-Identifier: MIT
# Copyright (c) 2026 gajsin
"""Build the source archive with per-skill licenses."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import zipfile

PLATFORMS = {'codex': 'Codex', 'antigravity': 'Antigravity', 'claude': 'Claude Code'}
BUNDLE_NAME = 'gajsin-skills.zip'
LOCATIONS = {
    'codex': '~/.agents/skills',
    'antigravity': '~/.gemini/config/skills',
    'claude': '~/.claude/skills',
}
ORIGINS = {
    **{name: 'https://github.com/mattpocock/skills/tree/5beb35b' for name in
       ['diagnosing-bugs', 'spec-review', 'codebase-design', 'grilling', 'retro']},
    'ponytail': 'https://github.com/DietrichGebert/ponytail/tree/09c434a',
    'caveman': 'https://github.com/juliusbrussee/caveman/tree/9b68f7ed12b05e7efaff18e65c5a3fc2849fd0a4',
    'humanizer': 'https://github.com/blader/humanizer/tree/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8',
    'editor': 'https://github.com/N1arko/redaktura-skills/tree/d1ebaff4fb8b97f939826a1cac284c10303be6f1',
    'impeccable': 'https://github.com/pbakaus/impeccable/tree/936867543ac2576920d663cc9803597f6044f3ac',
    **{name: 'https://github.com/greensock/gsap-skills/tree/aed9cfd3277740755f6bfc1155c7aa645403b760'
       for name in ['gsap']},
    **{name: 'https://github.com/gajsin/skills' for name in
       ['architecture-first', 'model-provider-qualification', 'logo-interview', 'visual-explainer']},
}
SKIP_DIRS = {'.git', '.cache', '__pycache__', 'node_modules', '.venv'}


def skill_dirs(root):
    if not root.is_dir():
        raise ValueError(f'Missing skill source directory: {root}')
    return sorted(p for p in root.iterdir() if p.is_dir() and (p / 'SKILL.md').is_file())


def skill_files(root):
    root = root.resolve()
    skills = {path.name for path in skill_dirs(root)}
    if not skills:
        raise ValueError('No skills found.')
    files = {}
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts) or path.suffix in {'.pyc', '.pyo'}:
            continue
        if path.is_symlink():
            raise ValueError(f'Resolve symlinks before packaging: {rel}')
        if not path.is_file():
            continue
        if len(rel.parts) < 2 or rel.parts[0] not in skills:
            raise ValueError(f'File has no skill directory: {path}')
        if root not in path.resolve().parents or any(part.startswith('.env') for part in rel.parts):
            raise ValueError(f'Unexpected source path: {rel}')
        if path.suffix.lower() in {'.exe', '.dll', '.so', '.dylib'}:
            raise ValueError(f'Runtime binaries do not belong in this source bundle: {rel}')
        files[rel.as_posix()] = path
    return files


def build_bundle(repo_root, output):
    root = (repo_root / 'skills').resolve()
    output = output.resolve()
    if root == output or root in output.parents:
        raise ValueError('The archive must be outside the skill source directory.')
    sources = skill_files(root)
    skills = sorted(name.removesuffix('/SKILL.md') for name in sources if name.count('/') == 1
                    and name.endswith('/SKILL.md'))
    files = []
    rows = []
    for skill in skills:
        if skill not in ORIGINS:
            raise ValueError(f'Add provenance for the new skill before packaging: {skill}')
        if f'{skill}/LICENSE' not in sources:
            raise ValueError(f'Missing LICENSE: {skill}')
        manifest = sources[f'{skill}/SKILL.md'].read_text(encoding='utf-8')
        license_match = re.search(r'^license:\s*(.+)$', manifest, re.M)
        if not license_match:
            raise ValueError(f'Missing license declaration: {skill}')
        license_name = license_match.group(1).strip().strip('\"\'')
        rows.append(f'| [{skill}](skills/{skill}/SKILL.md) | [{license_name}](skills/{skill}/LICENSE) | [Source]({ORIGINS[skill]}) |')
    files.extend((f'skills/{name}', path.read_bytes()) for name, path in sources.items())
    locations = '\n'.join(f'| {title} | `{LOCATIONS[host]}` |' for host, title in PLATFORMS.items())
    # GUIDE.md is the single source; its headings move one level down inside the README.
    guide = ''.join('#' + line if line.startswith('#') else line
                    for line in (repo_root / 'GUIDE.md').read_text(encoding='utf-8').splitlines(True))
    readme = f'''# Agent Skills

Reusable English instructions; agents should respond in the user's language.
Copy each complete directory you want from `skills/` into the skill directory for
your agent. Keep its license, references, and helpers together.

| Host | Skill directory |
|---|---|
{locations}

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
    return {'skills': len(skills), 'files': len(files),
            'sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'bytes': output.stat().st_size}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = build_bundle(Path(__file__).resolve().parents[1], args.output)
    print(json.dumps(result))
