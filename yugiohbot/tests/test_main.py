import unittest

import main


class TestMain(unittest.TestCase):
    def test_generate_effect(self):
        l = 'yugiohbot/resources/flavour_list.csv'
        test_templates = ['Normal', 'Effect', 'Spell', 'Trap', 'Fusion']
        for t in test_templates:
            e = main.generate_effect(t, l)
            self.assertTrue(e)

        e = main.generate_effect('Wrong', l)
        self.assertTrue(e == 'Oops! No Effect could be generated for this card. Destroy it.')


if __name__ == '__main__':
    unittest.main()
