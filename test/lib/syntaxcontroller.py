import unittest

from pysumo.syntaxcontroller import *
from pysumo.indexabstractor import IndexAbstractor
from pysumo.parser import kifparse, AbstractSyntaxTree

class syntaxTestCase(unittest.TestCase):
    def setUp(self):
        self.sumo = Ontology('data/Merge.kif', name='SUMO')
        self.milo = Ontology('data/MILO.kif', name='MILO')
        self.syntaxcontroller = SyntaxController(IndexAbstractor())

    def test0FirstOntology(self):
        self.assertEqual(self.syntaxcontroller.index.root, None)
        self.syntaxcontroller.add_ontology(self.sumo)
        self.assertNotEqual(self.syntaxcontroller.index.root, None)
        with open(self.sumo.path) as f:
            kif = kifparse(f, self.sumo)
            kif.ontology = None
        self.assertEqual(self.syntaxcontroller.index.root, kif)

    def test1RedundantAdd(self):
        self.syntaxcontroller.add_ontology(self.sumo)
        old_ast = self.syntaxcontroller.index.root
        self.syntaxcontroller.add_ontology(self.sumo)
        self.assertEqual(old_ast, self.syntaxcontroller.index.root)

    def test2WipeRemove(self):
        self.assertEqual(self.syntaxcontroller.index.root, None)
        self.syntaxcontroller.add_ontology(self.sumo)
        self.assertNotEqual(self.syntaxcontroller.index.root, None)
        self.syntaxcontroller.remove_ontology(self.sumo)
        self.assertEqual(self.syntaxcontroller.index.root, AbstractSyntaxTree(None))

    def test3AnotherAdd(self):
        self.syntaxcontroller.add_ontology(self.sumo)
        old_ast = self.syntaxcontroller.index.root
        self.syntaxcontroller.add_ontology(self.milo)
        self.assertNotEqual(self.syntaxcontroller.index.root, old_ast)
        sterm = self.syntaxcontroller.index.search('raNgesubclass')
        self.assertDictEqual(sterm, {self.sumo: ['( instance rangeSubclass BinaryPredicate )', '( instance rangeSubclass AsymmetricRelation )', '( domain rangeSubclass 1 Function )', '( domainSubclass rangeSubclass 2 SetOrClass )', '( documentation rangeSubclass EnglishLanguage "(&%rangeSubclass ?FUNCTION ?CLASS) means thatall of the values assigned by ?FUNCTION are &%subclasses of ?CLASS." )']})
        mterm = self.syntaxcontroller.index.search('organISMRemains')
        self.assertNotEqual(mterm, None)

    def test4GetOntologies(self):
        ontologies = get_ontologies(user='data')
        self.assertIn(Ontology('data/Merge.kif'), ontologies)
        self.assertIn(Ontology('data/MILO.kif'), ontologies)


syntaxTestSuit = unittest.makeSuite(syntaxTestCase, 'test')

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(syntaxTestSuit)
