# SPDX-License-Identifier: MIT
# Copyright (c) 2026 gajsin
"""Protect the public card contract in the release manifest."""
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

    def read(self, value, names=('first', 'second')):
        (self.root / 'catalog.json').write_text(json.dumps(value), encoding='utf-8')
        return publish_manifest.load_catalog(names)

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


if __name__ == '__main__':
    unittest.main()
