import csv
import os
import unittest

from title import *


class TestTitleGenerator(unittest.TestCase):
    test_csv_file = 'test.csv'

    def setUp(self):
        with open(self.test_csv_file, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(['id', 'card', 'desc'])
            filewriter.writerow([34541863, '"A" Cell Breeding Device'])
            filewriter.writerow([64163367, '"A" Cell Incubator'])
            filewriter.writerow([15308295, 'Abyss Actor - Comic Relief'])
            filewriter.writerow([6850209, 'A Deal with Dark Ruler'])
            filewriter.writerow([68170903, 'A Feint Plan'])

    def tearDown(self):
        os.remove(self.test_csv_file)

    def test_dedup(self):
        list = ['word', 'word', 'another', 'phrase', 'word', 'another', 'phrase']
        dedup_list = title.dedup(list)
        self.assertEqual(len(dedup_list), 3)

    def test_parse_existing_titles_valid_file(self):
        n, a = title.parse_existing_titles(self.test_csv_file)
        self.assertTrue(len(n) > 0)
        self.assertTrue(len(a) > 0)

    def test_parse_existing_titles_invalid_file(self):
        n, a = title.parse_existing_titles('badfile.csv')
        self.assertEqual(len(n), 0)
        self.assertEqual(len(a), 0)

    def test_create_new_title_valid_lists(self):
        nouns = ['book', 'tray', 'screen']
        adjectives = ['heavy', 'light']
        t = title.create_new_title(nouns, adjectives)
        self.assertTrue(any(word in t for word in nouns) or any(word in t for word in adjectives))

    def test_create_new_title_invalid_lists(self):
        t = title.create_new_title([], [])
        self.assertEqual(t, "")

    def test_create_new_title_invalid_nouns(self):
        adjectives = ['heavy', 'light']
        t = title.create_new_title([], adjectives)
        self.assertEqual(t, "")

    def test_create_new_title_invalid_adjectives(self):
        nouns = ['book', 'tray', 'screen']
        t = title.create_new_title(nouns, [])
        self.assertTrue(any(word in t for word in nouns))


if __name__ == '__main__':
    unittest.main()
