import atexit
import unittest

from copy import deepcopy
from io import StringIO
from pickle import dumps
from shutil import rmtree
from tempfile import mkdtemp

from pysumo.syntaxcontroller import *
from pysumo.indexabstractor import IndexAbstractor
from pysumo.parser import kifparse, AbstractSyntaxTree, astmerge
import pysumo

class syntaxTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = mkdtemp()
        self.sumo = Ontology('src/pysumo/data/Merge.kif', name='SUMO', lpath=self.tmpdir)
        self.milo = Ontology('src/pysumo/data/MILO.kif', name='MILO', lpath=self.tmpdir)
        self.syntaxcontroller = SyntaxController(IndexAbstractor())
        atexit.unregister(self.sumo.action_log.log_io.flush_write_queues)
        atexit.unregister(self.milo.action_log.log_io.flush_write_queues)

    def tearDown(self):
        atexit._clear()
        self.sumo.action_log.log_io.flush_write_queues()
        self.milo.action_log.log_io.flush_write_queues()
        rmtree(self.tmpdir)

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
        # Ignore changed action_log when comparing
        old_ast.children[0].ontology.action_log = self.sumo.action_log
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
        self.assertListEqual(sterm[self.sumo], [('( instance rangeSubclass BinaryPredicate )', 324), ('( instance rangeSubclass AsymmetricRelation )', 325), ('( domain rangeSubclass 1 Function )', 326), ('( domainSubclass rangeSubclass 2 SetOrClass )', 327), ('( documentation rangeSubclass EnglishLanguage "(&%rangeSubclass ?FUNCTION ?CLASS) means thatall of the values assigned by ?FUNCTION are &%subclasses of ?CLASS." )', 329)])
        mterm = self.syntaxcontroller.index.search('organISMRemains')
        self.assertListEqual(mterm[self.milo], [('( subclass OrganismRemains OrganicObject )', 138), ('( documentation OrganismRemains EnglishLanguage "An&%instance of &%OrganismRemains is &%Dead matter of aformerly &%Living &%Organism: &%Plant, &%Animal, or&%Microorganism.  An &%instance of &%OrganismRemains mightor might not be recognizable as the remains of a particularkind or species of organism, depending on the cause of the&%Organism\'s &%Death (heart failure, stroke, roadkill,dismemberment, etc.), the elapsed time since death, thespeed of decomposition, and any post-mortem processing ofthe dead organism (embalming, cremation, mummification,boiling, consumption as food, etc.)." )', 149)])

    def test4GetOntologies(self):
        ontologies = get_ontologies(lpath=self.tmpdir)
        for o in ontologies:
            atexit.unregister(o.action_log.log_io.flush_write_queues)
            o.action_log.log_io.flush_write_queues()
        a = Ontology('src/pysumo/data/Merge.kif', lpath=self.tmpdir)
        atexit.unregister(a.action_log.log_io.flush_write_queues)
        b = Ontology('src/pysumo/data/MILO.kif', lpath=self.tmpdir)
        atexit.unregister(b.action_log.log_io.flush_write_queues)
        self.assertIn(a, ontologies)
        self.assertIn(b, ontologies)
        a.action_log.log_io.flush_write_queues()
        b.action_log.log_io.flush_write_queues()

    def test5ParseAdd(self):
        self.syntaxcontroller.add_ontology(self.sumo)
        old_ast = deepcopy(self.syntaxcontroller.index.root)
        code_block = StringIO()
        with open(self.sumo.path) as code:
            code_block.write(code.read())
        code_block.write('(instance foo Entity)\n(documentation foo EnglishLanguage "&%foo is an object of type foo")\n')
        self.syntaxcontroller.add_ontology(self.sumo, code_block.getvalue())
        sterm = self.syntaxcontroller.index.search('foo')
        self.assertListEqual([x[0] for x in sterm[self.sumo]], ['( instance foo Entity )', '( documentation foo EnglishLanguage "&%foo is an object of type foo" )'])
        sio = StringIO('(instance foo Entity)\n(documentation foo EnglishLanguage "&%foo is an object of type foo")\n')
        ast = kifparse(sio, self.sumo)
        old_ast.children.extend(ast.children)
        self.assertEqual(len(self.syntaxcontroller.index.root.children), len(old_ast.children))

    def test6ParseDiff(self):
        self.syntaxcontroller.add_ontology(self.sumo)
        old_ast = deepcopy(self.syntaxcontroller.index.root)
        code_block = StringIO(_DIFF_ADD)
        self.syntaxcontroller.parse_patch(self.sumo, _DIFF_ADD)
        sterm = self.syntaxcontroller.index.search('foo')
        self.assertListEqual([x[0] for x in sterm[self.sumo]], ['( instance foo Entity )', '( documentation foo EnglishLanguage "&%foo is an object of type foo" )'])
        sio = StringIO('(instance foo Entity)\n(documentation foo EnglishLanguage "&%foo is an object of type foo")\n')
        ast = kifparse(sio, self.sumo)
        old_ast.children.extend(ast.children)
        self.assertEqual(len(self.syntaxcontroller.index.root.children), len(old_ast.children))
        self.syntaxcontroller.parse_patch(self.sumo, _DIFF_SUB)
        sterm = self.syntaxcontroller.index.search('foo')
        self.assertListEqual([x[0] for x in sterm[self.sumo]], list())
        self.assertRaises(KeyError, self.syntaxcontroller.index._find_term, 'foo')

    def test7UndoRedo(self):
        self.test5ParseAdd()
        self.syntaxcontroller.undo(self.sumo)
        sterm = self.syntaxcontroller.index.search('foo')
        self.assertListEqual([x[0] for x in sterm[self.sumo]], list())
        self.assertRaises(KeyError, self.syntaxcontroller.index._find_term, 'foo')
        self.syntaxcontroller.redo(self.sumo)
        sterm = self.syntaxcontroller.index.search('foo')
        self.assertListEqual([x[0] for x in sterm[self.sumo]], ['( instance foo Entity )', '( documentation foo EnglishLanguage "&%foo is an object of type foo" )'])

_DIFF_ADD = """
--- dev/kit/pse/pysumo/data/Merge.kif   2015-02-12 17:07:26.991461485 +0100
+++ test        2015-02-24 14:39:56.609460898 +0100
@@ -15672,3 +15672,5 @@
 ;;    (not
 ;;       (exists (?ITEM1 ?ITEM2 ?ITEM3 ?ITEM4 ?ITEM5 ?ITEM6 @ROW)
 ;;          (?REL ?ITEM1 ?ITEM2 ?ITEM3 ?ITEM4 ?ITEM5 ?ITEM6 @ROW))))
+(instance foo Entity)
+(documentation foo EnglishLanguage "&%foo is an object of type foo")
"""

_DIFF_SUB = """
--- dev/kit/pse/pysumo/data/Merge.kif   2015-02-12 17:07:26.991461485 +0100
+++ test        2015-02-24 14:39:56.609460898 +0100
@@ -15672,5 +15672,3 @@
 ;;    (not
 ;;       (exists (?ITEM1 ?ITEM2 ?ITEM3 ?ITEM4 ?ITEM5 ?ITEM6 @ROW)
 ;;          (?REL ?ITEM1 ?ITEM2 ?ITEM3 ?ITEM4 ?ITEM5 ?ITEM6 @ROW))))
-(instance foo Entity)
-(documentation foo EnglishLanguage "&%foo is an object of type foo")
"""

syntaxTestSuit = unittest.makeSuite(syntaxTestCase, 'test')

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(syntaxTestSuit)
