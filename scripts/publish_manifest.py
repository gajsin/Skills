# SPDX-License-Identifier: MIT
# Copyright (c) 2026 gajsin
"""Build the three host archives and skills.json, the manifest that gajsin.tech reads from the release."""
from pathlib import Path
import argparse
import json
import re
import subprocess

from package_skills import LOCATIONS, ORIGINS, PLATFORMS, build_bundle, skill_dirs

REPO = Path(__file__).resolve().parents[1]
CARD_FIELDS = {'group', 'use', 'result', 'edits'}


def load_catalog():
    """Require a complete card for each skill in each host edition."""
    catalog = json.loads((REPO / 'catalog.json').read_text(encoding='utf-8'))
    if not isinstance(catalog, dict):
        raise ValueError('catalog.json must contain an object keyed by skill name')
    card_names = set(catalog)
    for edition in PLATFORMS.values():
        directory = REPO / edition / 'skills'
        skill_names = {path.name for path in skill_dirs(directory)}
        missing = sorted(card_names - skill_names)
        extra = sorted(skill_names - card_names)
        if missing or extra:
            raise ValueError(f'catalog.json does not match {edition}: missing skills={missing}, extra skills={extra}')
    for name, card in catalog.items():
        if not isinstance(card, dict) or set(card) != CARD_FIELDS:
            raise ValueError(f'{name}: the catalogue card must have group, use, result and edits')
        for key, value in card.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f'{name}: catalogue {key} must be non-empty text')
    return catalog


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
    folder = REPO / PLATFORMS['claude'] / 'skills'
    catalog = load_catalog()
    skills = []
    for name, card in catalog.items():
        text = (folder / name / 'SKILL.md').read_text(encoding='utf-8')
        skills.append({'name': name, 'description': field(text, 'description', name),
                       'license': field(text, 'license', name), 'origin': ORIGINS[name], **card})
    packs = []
    for platform, title in PLATFORMS.items():
        name = f'gajsin-skills-{platform}.zip'
        result = build_bundle(REPO, platform, output / name)
        packs.append({'platform': platform, 'title': title, 'url': f'{download_base}/{name}',
                      'bytes': result['bytes'], 'sha256': result['sha256'],
                      'location': LOCATIONS[platform], 'invoke': '$' if platform == 'codex' else '/'})
    # One journal entry per day: which skills changed in any host edition.
    updates = []
    log = git('log', '--date=short', '--format=%x1e%cs', '--name-only', '--',
              *(f'{edition}/skills' for edition in PLATFORMS.values()))
    for block in filter(None, log.split('\x1e')):
        day, *files = block.strip().split('\n')
        changed = sorted({parts[2] for parts in (path.split('/') for path in files) if len(parts) > 3 and parts[2] in catalog})
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
