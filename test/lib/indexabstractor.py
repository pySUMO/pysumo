""" The PyUnit test framework for the indexabstractor. """

import unittest

from io import StringIO
from pysumo import parser
from pysumo.indexabstractor import *
from pysumo.syntaxcontroller import Ontology

class indexTestCase(unittest.TestCase):
    def setUp(self):
        self.sumo = Ontology('data/Merge.kif', name='SUMO')
        with open(self.sumo.path) as f:
            self.kif = parser.kifparse(f, self.sumo)
        self.indexabstractor = IndexAbstractor()
        self.indexabstractor.update_index(self.kif)

    def test0Normalize(self):
        self.assertEqual(normalize('t.erm '), 'term')
        self.assertEqual(normalize('  TeRM    '), 'term')
        self.assertNotEqual(normalize('t erm  '), 'term')

    def test1BuildIndex(self):
        self.assertEqual(self.indexabstractor.ontologies, {self.sumo})
        self.assertEqual(self.indexabstractor.root, self.kif)

    def test2Search(self):
        self.maxDiff = None
        self.assertEqual(self.indexabstractor.search('Plasma'),
                         self.indexabstractor.search('plasma'))
        self.assertEqual(self.indexabstractor.search('ValidDeductiveArgument'),
                         self.indexabstractor.search(' valIddedUctiVeargument   '))
        self.assertNotEqual(self.indexabstractor.search('ValidDeductiveArgument'),
                            self.indexabstractor.search('InvalidDeductiveArgument'))
        result = self.indexabstractor.search(' ContentbearingObJect')
        self.assertIn(self.sumo, result)
        definition = result[self.sumo]
        self.assertEqual(sorted(definition),
                sorted(['( relatedInternalConcept ContentBearingObject containsInformation )',
                 '( subclass ContentBearingObject CorpuscularObject )',
                 '( subclass ContentBearingObject ContentBearingPhysical )',
                 '( documentation ContentBearingObject EnglishLanguage "Any &%SelfConnectedObject that expressescontent.  This content may be a &%Proposition, e.g. when the &%ContentBearingObjectis a &%Sentence or &%Text, or it may be a representation of an abstract orphysical object, as with an &%Icon, a &%Word or a &%Phrase." )']))

    def test3WordNet(self):
        self.assertEqual(self.indexabstractor.wordnet, None)
        self.assertEqual(len(self.indexabstractor.wordnet_locate('   enTiTy     ')), 31)
        self.assertNotEqual(self.indexabstractor.wordnet, None)

    def test4AbstractGraph(self):
        graph = self.indexabstractor.get_graph('Ontology')
        self.assertIn(AbstractGraphNode(self.sumo), graph.nodes)
        graph = self.indexabstractor.get_graph('subrelation', 'subclass')
        self.assertEqual(graph.nodes, ['immediateSubclass', 'subset', 'subclass'])
        self.assertEqual(graph.relations, {'subclass': {'subset', 'immediateSubclass'}})
        graph = self.indexabstractor.get_graph('subclass', 'entity')
        self.assertEqual(len(graph.nodes), 660)
        self.assertEqual(len(graph.relations), 266)
        graph = self.indexabstractor.get_graph('subclass', 'entity', 3)
        self.assertEqual(len(graph.nodes), 186)
        self.assertEqual(len(graph.relations), 122)

    def test5GetOntology(self):
        of = self.indexabstractor.get_ontology_file(self.sumo)
        o_ast = parser.kifparse(of, self.sumo)
        with open(self.sumo.path) as sumo:
            s_ast = parser.kifparse(sumo, self.sumo)
        self.assertEqual(o_ast, s_ast)

indexTestSuit = unittest.makeSuite(indexTestCase, 'test')

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(indexTestSuit)
