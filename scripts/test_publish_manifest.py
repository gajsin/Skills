# SPDX-License-Identifier: MIT
# Copyright (c) 2026 gajsin
"""Protect the public card contract used by the portfolio's release reader."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest
from unittest.mock import patch

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
        for edition in publish_manifest.PLATFORMS.values():
            for name in ('first', 'second'):
                skill = self.root / edition / 'skills' / name
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

    def test_missing_skill_in_non_claude_pack_blocks_publication(self):
        (self.root / 'Antigravity/skills/second/SKILL.md').unlink()
        with self.assertRaisesRegex(ValueError, r"Antigravity: missing skills=\['second'\]"):
            self.read({'first': self.card, 'second': self.card})

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


if __name__ == '__main__':
    unittest.main()
