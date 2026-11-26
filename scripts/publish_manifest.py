# SPDX-License-Identifier: MIT
# Copyright (c) 2026 gajsin
"""Build the three host archives and skills.json, the manifest that gajsin.tech reads from the release."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import re
import subprocess

from package_skills import LOCATIONS, ORIGINS, PLATFORMS, build_bundle, skill_dirs

REPO = Path(__file__).resolve().parents[1]
CARD_FIELDS = {'group', 'use', 'result', 'edits'}
JOURNAL_PATHS = (*(f'{edition}/skills' for edition in PLATFORMS.values()), 'catalog.json')
JOURNAL_SIZE = 20


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


def journal_changes(commit, previous=None):
    """Keep published entries and add relevant commits since the last published SHA."""
    old_changes = []
    revision = commit
    if previous is not None and 'changes' in previous:
        source = previous['source']
        old_commit = source['commit']
        if source['repository'] != 'gajsin/Skills' or not re.fullmatch(r'[0-9a-f]{40}', old_commit):
            raise ValueError('Previous skills.json has an invalid source')
        try:
            ancestor = git('merge-base', old_commit, commit) == old_commit
        except subprocess.CalledProcessError as error:
            if error.returncode not in (1, 128):
                raise
            ancestor = False
        if ancestor:
            revision = f'{old_commit}..{commit}'
            old_changes = previous['changes']

    log = git('log', '-z', f'-{JOURNAL_SIZE}', '--format=%H%x00%cI%x00%B', revision, '--', *JOURNAL_PATHS)
    fields = log.removesuffix('\x00').split('\x00') if log else []
    changes = []
    for sha, date, message in zip(fields[::3], fields[1::3], fields[2::3], strict=True):
        title, _, body = message.strip().partition('\n')
        body = re.sub(r'(?:^|\n\n)(?:Co-Authored-By:[^\n]+(?:\n|$))+$', '', body.strip(), flags=re.I)
        utc_date = datetime.fromisoformat(date).astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        changes.append({'sha': sha, 'date': utc_date, 'title': title or sha[:7], 'body': body})
    unique = {change['sha']: change for change in [*changes, *old_changes]}
    return sorted(unique.values(), key=lambda change: change['date'], reverse=True)[:JOURNAL_SIZE]


def build_manifest(output, download_base, previous=None):
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
                'packs': packs, 'skills': skills, 'updates': updates[:12],
                'changes': journal_changes(commit, previous)}
    (output / 'skills.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--download-base', required=True, help='URL prefix of the release assets')
    parser.add_argument('--previous-manifest', type=Path, help='skills.json from the currently published release')
    args = parser.parse_args()
    previous = json.loads(args.previous_manifest.read_text(encoding='utf-8')) if args.previous_manifest else None
    manifest = build_manifest(args.output.resolve(), args.download_base.rstrip('/'), previous)
    print(json.dumps({'commit': manifest['source']['commit'][:7], 'skills': len(manifest['skills'])}))
