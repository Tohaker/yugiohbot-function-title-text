import csv
import os
import unittest

from text import *


class TestTextGenerator(unittest.TestCase):
    test_csv_file = 'test.csv'

    def setUp(self):
        with open(self.test_csv_file, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(['id', 'card', 'desc'])
            filewriter.writerow([34541863, '"A" Cell Breeding Device',
                                 "During each of your Standby Phases, put 1 A-Counter on 1 face-up monster your opponent controls."
                                 ])
            filewriter.writerow([64163367, '"A" Cell Incubator',
                                 "Each time an A-Counter(s) is removed from play by a card effect, place 1 A-Counter on this card. When this card is destroyed, distribute the A-Counters on this card among face-up monsters."
                                 ])
            filewriter.writerow(['91231901', '"A" Cell Recombination Device',
                                 "Target 1 face-up monster on the field; send 1 ""Alien"" monster from your Deck to the Graveyard, and if you do, place A-Counters on that monster equal to the Level of the sent monster. During your Main Phase, except the turn this card was sent to the Graveyard: You can banish this card from your Graveyard; add 1 ""Alien"" monster from your Deck to your hand."
                                 ])
            filewriter.writerow(
                [6850209, 'A Deal with Dark Ruler', '"(This card is always treated as an ""Archfiend"" card.)'
                 ])
            filewriter.writerow([68170903, 'A Feint Plan', 'A player cannot attack face-down monsters during this turn.'
                                 ])

    def tearDown(self):
        os.remove(self.test_csv_file)

    def test_split_description_with_valid_csv(self):
        phrases = text.split_descriptions(self.test_csv_file)
        self.assertEqual(len(phrases), 5)

    def test_split_description_with_invalid_csv(self):
        phrases = text.split_descriptions('badfile.csv')
        self.assertEqual(len(phrases), 0)

    def test_generate_card_text_with_five_valid_phrases(self):
        phrases = [['here.', 'are.'], ['some.', 'phrases,'], ['that;', 'will:'], ['work.'], ['I.', 'hope,']]
        t = text.generate_card_text(phrases)
        self.assertTrue(t != "")
        self.assertTrue(t[-1:] != ",")

    def test_generate_card_text_fewer_than_five_valid_phrases(self):
        phrases = [['some', 'phrases'], ['that', 'will'], ['work', 'I', 'hope']]
        t = text.generate_card_text(phrases)
        self.assertTrue(t != "")

    def test_generate_card_text_empty_phrases(self):
        phrases = []
        t = text.generate_card_text(phrases)
        self.assertTrue(t == "")


if __name__ == '__main__':
    unittest.main()
