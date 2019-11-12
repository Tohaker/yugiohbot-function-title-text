import unittest

from text import ml_text


class TestMLText(unittest.TestCase):
    def test_generate_card_description(self):
        test_templates = ['fusion', 'monster', 'spell', 'trap']
        for t in test_templates:
            d = ml_text.generate_card_description(t)
            self.assertTrue(d)

        d = ml_text.generate_card_description('wrong')
        self.assertEqual(d, None)

    def test_format_punctuation(self):
        input = 'here . Are , some ; words : that - should ( be tested )'
        expected = 'here. Are, some; words: that-should (be tested)'
        actual = ml_text.format_punctuation(input)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
