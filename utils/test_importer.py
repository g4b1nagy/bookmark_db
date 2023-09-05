import json
import unittest

from utils.importer import get_bookmarks_and_labels


class TestImporter(unittest.TestCase):

    def test_importer(self):
        self.maxDiff = None
        bookmarks, labels = get_bookmarks_and_labels('utils/test_files/')
        for bookmark in bookmarks.values():
            bookmark['labels'] = sorted(bookmark['labels'])
        actual_bookmarks = json.dumps(bookmarks, indent=4, sort_keys=True)
        actual_labels = json.dumps(labels, indent=4, sort_keys=True)
        with open('utils/test_files/expected_bookmarks.json') as f:
            expected_bookmarks = f.read()
        with open('utils/test_files/expected_labels.json') as f:
            expected_labels = f.read()
        self.assertEqual(actual_bookmarks, expected_bookmarks)
        self.assertEqual(actual_labels, expected_labels)
