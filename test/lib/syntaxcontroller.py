import unittest

from copy import deepcopy
from pickle import dumps

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
        old_ast = deepcopy(self.syntaxcontroller.index.root)
        self.syntaxcontroller.add_ontology(self.sumo)
        x = deepcopy(old_ast.children[0])
        y = deepcopy(self.syntaxcontroller.index.root.children[0])
        self.assertEqual(dumps(x), dumps(y))
        self.assertEqual(old_ast.name, self.syntaxcontroller.index.root.name)
        self.assertEqual(old_ast.element_type, self.syntaxcontroller.index.root.element_type)
        self.assertEqual(old_ast.ontology, self.syntaxcontroller.index.root.ontology)
        self.assertEqual(old_ast.line, self.syntaxcontroller.index.root.line)
        self.assertEqual(old_ast.children[0].name, self.syntaxcontroller.index.root.children[0].name)
        self.assertEqual(old_ast.children[0].element_type, self.syntaxcontroller.index.root.children[0].element_type)
        self.assertEqual(old_ast.children[0].ontology, self.syntaxcontroller.index.root.children[0].ontology)
        self.assertEqual(old_ast.children[0].line, self.syntaxcontroller.index.root.children[0].line)
        self.assertEqual(old_ast.children[0].children, self.syntaxcontroller.index.root.children[0].children)
        self.assertEqual(old_ast.children[0], self.syntaxcontroller.index.root.children[0])
        self.assertListEqual(old_ast.children, self.syntaxcontroller.index.root.children)
        self.assertEqual(old_ast, self.syntaxcontroller.index.root)

    def test2WipeRemove(self):
        self.assertEqual(self.syntaxcontroller.index.root, None)
        self.syntaxcontroller.add_ontology(self.sumo)
        self.assertNotEqual(self.syntaxcontroller.index.root, None)
        self.syntaxcontroller.remove_ontology(self.sumo)
        self.assertEqual(self.syntaxcontroller.index.root, AbstractSyntaxTree(None))

    def test3AnotherAdd(self):
        self.maxDiff = None
        self.syntaxcontroller.add_ontology(self.sumo)
        old_ast = deepcopy(self.syntaxcontroller.index.root)
        self.assertNotEqual(old_ast, AbstractSyntaxTree(None))
        self.syntaxcontroller.add_ontology(self.milo)
        self.assertNotEqual(self.syntaxcontroller.index.root, old_ast)
        sterm = self.syntaxcontroller.index.search('raNgesubclass')
        self.assertListEqual(sterm[self.sumo], ['( instance rangeSubclass BinaryPredicate )', '( instance rangeSubclass AsymmetricRelation )', '( domain rangeSubclass 1 Function )', '( domainSubclass rangeSubclass 2 SetOrClass )', '( documentation rangeSubclass EnglishLanguage "(&%rangeSubclass ?FUNCTION ?CLASS) means thatall of the values assigned by ?FUNCTION are &%subclasses of ?CLASS." )'])
        mterm = self.syntaxcontroller.index.search('organISMRemains')
        self.assertListEqual(mterm[self.milo], ['( subclass OrganismRemains OrganicObject )', '( documentation OrganismRemains EnglishLanguage "An&%instance of &%OrganismRemains is &%Dead matter of aformerly &%Living &%Organism: &%Plant, &%Animal, or&%Microorganism.  An &%instance of &%OrganismRemains mightor might not be recognizable as the remains of a particularkind or species of organism, depending on the cause of the&%Organism\'s &%Death (heart failure, stroke, roadkill,dismemberment, etc.), the elapsed time since death, thespeed of decomposition, and any post-mortem processing ofthe dead organism (embalming, cremation, mummification,boiling, consumption as food, etc.)." )'])

    def test4GetOntologies(self):
        ontologies = get_ontologies(user='data')
        self.assertIn(Ontology('data/Merge.kif'), ontologies)
        self.assertIn(Ontology('data/MILO.kif'), ontologies)


syntaxTestSuit = unittest.makeSuite(syntaxTestCase, 'test')

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(syntaxTestSuit)
