""" The PyUnit test framework for the indexabstractor. """

import unittest

from pysumo.parser import SSType
from pysumo.wordnet import WordNet

class WordNetTestCase(unittest.TestCase):
    def setUp(self):
        self.wordnet = WordNet()

    def test0WordNet(self):
        self.assertEqual(self.wordnet.locate_term('PrivateDetective'),
                [('private_detective', SSType.noun, 'someone who can be employed as a detective to collect information')])
        self.assertEqual(len(self.wordnet.locate_term('Entity')), 31)

    def test1Synonyms(self):
        self.assertEqual(self.wordnet.find_synonym('table'),
                {'IntentionalProcess', 'Mesa', 'ContentDevelopment', 'Table', 'ContentBearingObject', 'Food', 'Meeting'})

WNTestSuit = unittest.makeSuite(WordNetTestCase, 'test')

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(WNTestSuit)
