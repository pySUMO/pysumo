""" The PyUnit test framework for the indexabstractor. """

import unittest

from lib import parser
from lib.indexabstractor import *

class indexTestCase(unittest.TestCase):
    def setUp(self):
        self.sumo = parser.Ontology('data/Merge.kif', name='SUMO')
        self.kif = parser.kifparse(self.sumo)
        self.indexabstractor = IndexAbstractor()

    def test0Normalize(self):
        self.assertEqual(normalize('t.erm '), 'term')
        self.assertEqual(normalize('  TeRM    '), 'term')
        self.assertNotEqual(normalize('t erm  '), 'term')

    def test1BuildIndex(self):
        self.indexabstractor.update_index(self.kif)
        self.assertEqual(self.indexabstractor.ontologies, {self.sumo})
        self.assertEqual(self.indexabstractor.root, self.kif)
        assert self.sumo in self.indexabstractor.index

    def test2Search(self):
        self.maxDiff = None
        self.indexabstractor.update_index(self.kif)
        self.assertEqual(self.indexabstractor.search('Plasma'),
                         self.indexabstractor.search('plasma'))
        self.assertEqual(self.indexabstractor.search('ValidDeductiveArgument'),
                         self.indexabstractor.search(' valIddedUctiVeargument   '))
        self.assertNotEqual(self.indexabstractor.search('ValidDeductiveArgument'),
                            self.indexabstractor.search('InvalidDeductiveArgument'))
        result = self.indexabstractor.search(' ContentbearingObJect')
        assert self.sumo in result
        definition = result[self.sumo]
        self.assertEqual(sorted(definition),
                sorted(['( relatedInternalConcept ContentBearingObject containsInformation )',
                 '( subclass ContentBearingObject CorpuscularObject )',
                 '( subclass ContentBearingObject ContentBearingPhysical )',
                 '( documentation ContentBearingObject EnglishLanguage "Any &%SelfConnectedObject that expressescontent.  This content may be a &%Proposition, e.g. when the &%ContentBearingObjectis a &%Sentence or &%Text, or it may be a representation of an abstract orphysical object, as with an &%Icon, a &%Word or a &%Phrase." )']))

indexTestSuit = unittest.makeSuite(indexTestCase, 'test')

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(indexTestSuit)
