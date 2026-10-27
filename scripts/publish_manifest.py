# SPDX-License-Identifier: MIT
# Copyright (c) 2026 gajsin
"""Build the three host archives and skills.json, the manifest that gajsin.tech reads from the release."""
from pathlib import Path
import argparse
import json
import re
import subprocess

from package_skills import LOCATIONS, ORIGINS, PLATFORMS, build_bundle

REPO = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.run(['git', '-C', str(REPO), *args], check=True, capture_output=True, text=True,
                          encoding='utf-8').stdout.strip()


def field(text, key, name):
    match = re.search(rf'^{key}:\s*(.+)$', text, re.M)
    if not match:
        raise ValueError(f'{name}/SKILL.md has no {key}')
    return match.group(1).strip().strip('"\'')


def build_manifest(output, download_base):
    commit, date = git('log', '-1', '--format=%H %cs').split(' ')
    packs = []
    for platform, title in PLATFORMS.items():
        name = f'gajsin-skills-{platform}.zip'
        result = build_bundle(REPO, platform, output / name)
        packs.append({'platform': platform, 'title': title, 'url': f'{download_base}/{name}',
                      'bytes': result['bytes'], 'sha256': result['sha256'],
                      'location': LOCATIONS[platform], 'invoke': '$' if platform == 'codex' else '/'})
    folder = REPO / PLATFORMS['claude'] / 'skills'
    names = sorted(path.name for path in folder.iterdir() if (path / 'SKILL.md').is_file())
    skills = []
    for name in names:
        text = (folder / name / 'SKILL.md').read_text(encoding='utf-8')
        skills.append({'name': name, 'description': field(text, 'description', name),
                       'license': field(text, 'license', name), 'origin': ORIGINS[name]})
    # One journal entry per day: which skills changed in any host edition.
    updates = []
    log = git('log', '--date=short', '--format=%x1e%cs', '--name-only', '--',
              *(f'{edition}/skills' for edition in PLATFORMS.values()))
    for block in filter(None, log.split('\x1e')):
        day, *files = block.strip().split('\n')
        changed = sorted({parts[2] for parts in (path.split('/') for path in files) if len(parts) > 3 and parts[2] in names})
        if not changed:
            continue
        if updates and updates[-1]['date'] == day:
            updates[-1]['skills'] = sorted(set(updates[-1]['skills']) | set(changed))
        else:
            updates.append({'date': day, 'skills': changed})
    manifest = {'source': {'repository': 'gajsin/Skills', 'commit': commit, 'date': date},
                'packs': packs, 'skills': skills, 'updates': updates[:12]}
    (output / 'skills.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--download-base', required=True, help='URL prefix of the release assets')
    args = parser.parse_args()
    manifest = build_manifest(args.output.resolve(), args.download_base.rstrip('/'))
    print(json.dumps({'commit': manifest['source']['commit'][:7], 'skills': len(manifest['skills'])}))
