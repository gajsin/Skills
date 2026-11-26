# SPDX-License-Identifier: MIT
# Copyright (c) 2026 gajsin
"""Protect the public card contract used by the portfolio's release reader."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import unittest
from unittest.mock import patch
from zipfile import ZipFile

import publish_manifest


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        patcher = patch.object(publish_manifest, 'REPO', self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.card = {'group': 'Дизайн', 'use': 'Задача', 'result': 'Результат', 'edits': 'Границы'}
        for name in ('first', 'second'):
            skill = self.root / 'skills' / name
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').touch()

    def read(self, value):
        (self.root / 'catalog.json').write_text(json.dumps(value), encoding='utf-8')
        return publish_manifest.load_catalog()

    def test_release_keeps_editorial_order_and_complete_cards(self):
        cards = {'second': self.card, 'first': {**self.card, 'group': 'Новая категория'}}
        result = self.read(cards)
        self.assertEqual(list(result), ['second', 'first'])
        self.assertEqual(result, cards)

    def test_missing_and_removed_skills_block_publication(self):
        for cards in ({'first': self.card}, {'first': self.card, 'second': self.card, 'removed': self.card}):
            with self.subTest(cards=cards), self.assertRaisesRegex(ValueError, 'does not match'):
                self.read(cards)

    def test_invalid_card_fields_block_publication(self):
        bad_cards = [None, [], {**self.card, 'extra': 'unsupported'}]
        for key in self.card:
            bad_cards.append({k: v for k, v in self.card.items() if k != key})
            bad_cards.extend({**self.card, key: value} for value in ('', '  ', None, 1, [], {}))
        for card in bad_cards:
            with self.subTest(card=card), self.assertRaises(ValueError):
                self.read({'first': self.card, 'second': card})

    def test_invalid_catalogue_root_is_rejected(self):
        for value in (None, [], 'text'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.read(value)


class JournalTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        repo = patch.object(publish_manifest, 'REPO', self.root)
        repo.start()
        self.addCleanup(repo.stop)
        self.git = publish_manifest.git
        self.git('init', '--quiet')
        self.git('config', 'user.name', 'Journal test')
        self.git('config', 'user.email', 'journal@example.test')

    def commit(self, title, *paths, body=''):
        for path in paths:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(title, encoding='utf-8')
        self.git('add', '--', *paths)
        self.git('commit', '--quiet', '--no-gpg-sign', '-m', title, '-m', body)
        return self.git('rev-parse', 'HEAD')

    def test_adds_only_new_skill_commits_and_keeps_published_entries(self):
        first = self.commit('Initial skill', 'Codex/skills/demo/SKILL.md')
        previous = {'source': {'repository': 'gajsin/Skills', 'commit': first}, 'changes': publish_manifest.journal_changes(first)}
        previous['changes'][0]['body'] = 'Already published'
        second = self.commit('Synchronize editions', 'Codex/skills/demo/SKILL.md', 'Claude Code/skills/demo/SKILL.md',
                             body='Updated examples.\n\nCo-Authored-By: Contributor <journal@example.test>')
        self.commit('Maintenance', 'README.md')
        third = self.commit('Update catalogue', 'catalog.json')
        journal = publish_manifest.journal_changes(third, previous)
        self.assertEqual([entry['sha'] for entry in journal], [third, second, first])
        self.assertEqual(journal[1]['body'], 'Updated examples.')
        self.assertEqual(journal[2]['body'], 'Already published')
        published = {'source': {'repository': 'gajsin/Skills', 'commit': third}, 'changes': journal}
        self.assertEqual(publish_manifest.journal_changes(third, published), journal)

    def test_first_release_and_rewritten_history_use_the_current_ancestry(self):
        first = self.commit('Add skill', 'Antigravity/skills/demo/SKILL.md')
        replaced = self.commit('Old release', 'catalog.json')
        previous = {'source': {'repository': 'gajsin/Skills', 'commit': replaced}, 'changes': publish_manifest.journal_changes(replaced)}
        self.git('checkout', '--quiet', '--detach', first)
        last = self.commit('Replacement release', 'catalog.json')
        self.assertEqual([entry['sha'] for entry in publish_manifest.journal_changes(last, previous)], [last, first])

    def test_skips_packaging_migration_and_finds_changes_at_both_new_paths(self):
        first = self.commit('Add skill', 'Antigravity/skills/old/SKILL.md')
        previous = {'source': {'repository': 'gajsin/Skills', 'commit': first}, 'changes': publish_manifest.journal_changes(first)}
        self.commit('Reorganize packaging', 'skills/moved/SKILL.md', body='Skill-Journal: skip')
        shared = self.commit('Improve shared skill', 'skills/shared/SKILL.md')
        platform = self.commit('Improve platform skill', 'platforms/codex/skills/native/SKILL.md')
        self.assertEqual([entry['sha'] for entry in publish_manifest.journal_changes(platform, previous)],
                         [platform, shared, first])
        changed = publish_manifest.skill_updates(dict.fromkeys(('old', 'moved', 'shared', 'native')))
        self.assertEqual({name for entry in changed for name in entry['skills']}, {'old', 'shared', 'native'})

    def test_release_serves_the_same_archive_at_existing_download_urls(self):
        card = {'group': 'Writing', 'use': 'Edit', 'result': 'Draft', 'edits': 'Requested text'}
        skill = self.root / 'skills/humanizer'
        skill.mkdir(parents=True)
        text = b'---\nname: humanizer\ndescription: Edit prose.\nlicense: MIT\n---\n'
        (skill / 'SKILL.md').write_bytes(text)
        (skill / 'LICENSE').touch()
        (self.root / 'scripts').mkdir()
        (self.root / 'scripts/LICENSE').touch()
        (self.root / 'GUIDE.md').write_text('# Guide\n', encoding='utf-8')
        (self.root / 'catalog.json').write_text(json.dumps({'humanizer': card}), encoding='utf-8')
        self.git('add', '.')
        self.git('commit', '--quiet', '--no-gpg-sign', '-m', 'Add skill')

        output = self.root / 'release'
        base = 'https://example.test/release'
        manifest = publish_manifest.build_manifest(output, base)
        archive = output / 'gajsin-skills.zip'
        self.assertEqual(set(output.iterdir()), {archive, output / 'skills.json',
                                               *(output / f'gajsin-skills-{host}.zip'
                                                 for host in ('codex', 'claude', 'antigravity'))})
        self.assertEqual(manifest['skills'][0]['description'], 'Edit prose.')
        self.assertEqual({p['platform'] for p in manifest['packs']}, {'codex', 'claude', 'antigravity'})
        data = archive.read_bytes()
        for pack in manifest['packs']:
            name = f'gajsin-skills-{pack["platform"]}.zip'
            self.assertEqual(pack['url'], f'{base}/{name}')
            self.assertEqual((output / name).read_bytes(), data)
            self.assertEqual(pack['sha256'], hashlib.sha256(data).hexdigest())
        with ZipFile(archive) as packed:
            self.assertEqual(packed.read('skills/humanizer/SKILL.md'), text)


if __name__ == '__main__':
    unittest.main()
