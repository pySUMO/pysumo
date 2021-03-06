""" The PyUnit test framework for the indexabstractor. """

import atexit
import unittest
from tempfile import mkdtemp
from shutil import rmtree
import pysumo

from io import StringIO
from pysumo import parser
from pysumo.indexabstractor import *
from pysumo.syntaxcontroller import Ontology

class indexTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = mkdtemp()
        self.sumo = Ontology('src/pysumo/data/Merge.kif', name='SUMO', lpath=self.tmpdir)
        atexit.unregister(self.sumo.action_log.log_io.flush_write_queues)
        with open(self.sumo.path) as f:
            self.kif = parser.kifparse(f, self.sumo)
        self.indexabstractor = IndexAbstractor()
        self.indexabstractor.update_index(self.kif)

    def tearDown(self):
        self.sumo.action_log.log_io.flush_write_queues()
        rmtree(self.tmpdir)

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
        definition = [x[0] for x in result[self.sumo]]
        self.assertListEqual(sorted(definition),
                sorted(['( relatedInternalConcept ContentBearingObject containsInformation )',
                 '( subclass ContentBearingObject CorpuscularObject )',
                 '( subclass ContentBearingObject ContentBearingPhysical )',
                 '( documentation ContentBearingObject EnglishLanguage "Any &%SelfConnectedObject that expressescontent.  This content may be a &%Proposition, e.g. when the &%ContentBearingObjectis a &%Sentence or &%Text, or it may be a representation of an abstract orphysical object, as with an &%Icon, a &%Word or a &%Phrase." )']))

    def test3WordNet(self):
        self.assertEqual(self.indexabstractor.wordnet, None)
        self.assertEqual(len(self.indexabstractor.wordnet_locate('   enTiTy     ')), 31)
        self.assertIn('electric_chair (n): an instrument of execution by electrocution; resembles an ordinary seat for one person; "the murderer was sentenced to die in the chair"', self.indexabstractor.wordnet_locate('chair'))
        self.assertNotEqual(self.indexabstractor.wordnet, None)

    def test4AbstractGraph(self):
        graph = self.indexabstractor.get_graph(None)
        self.assertIn(AbstractGraphNode(self.sumo), graph.nodes)
        graph = self.indexabstractor.get_graph([(0, 'subrelation')], root='subclass')
        self.assertEqual(graph.nodes, ['immediateSubclass', 'subset', 'subclass'])
        self.assertEqual(graph.relations, {'subclass': {'subset', 'immediateSubclass'}})
        graph = self.indexabstractor.get_graph([(0, 'subclass')], root='entity')
        self.assertEqual(len(graph.nodes), 660)
        self.assertEqual(len(graph.relations), 266)
        graph = self.indexabstractor.get_graph([(0, 'subclass')], root='entity', depth=3)
        self.assertEqual(len(graph.nodes), 65)
        self.assertEqual(len(graph.relations), 46)
        graph = self.indexabstractor.get_graph([(0, 'subclass')], root='entity', depth=0)
        self.assertEqual(len(graph.nodes), 1)
        self.assertEqual(len(graph.relations), 1)
        self.assertEqual(len(graph.relations['Entity']), 2)
        graph = self.indexabstractor.get_graph([(0, 'domain'), (1, 'instance')], major=1, minor=3)
        self.assertEqual(len(graph.nodes), 3)
        self.assertEqual(len(graph.relations), 1)
        self.assertEqual(len(graph.relations['instance']), 2)

    def test5GetOntology(self):
        of = self.indexabstractor.get_ontology_file(self.sumo)
        o_ast = parser.kifparse(of, self.sumo)
        with open(self.sumo.path) as sumo:
            s_ast = parser.kifparse(sumo, self.sumo)
        self.assertEqual(o_ast, s_ast)

    def test6MultipleOntologies(self):
        milo = Ontology('src/pysumo/data/MILO.kif', lpath=self.tmpdir)
        atexit.unregister(milo.action_log.log_io.flush_write_queues)
        with open(milo.path) as f:
            milo_kif = parser.kifparse(f, milo)
        merged_asts = parser.astmerge((self.kif, milo_kif))
        search_results = self.indexabstractor.search('rangesubclass')[self.sumo]
        self.indexabstractor.update_index(merged_asts)
        new_results = self.indexabstractor.search('rangesubclass')[self.sumo]
        self.assertListEqual(search_results, new_results)
        milo.action_log.log_io.flush_write_queues()

    def test7GetCompletions(self):
        completions = self.indexabstractor.get_completions()
        self.assertIn('TwoDimensionalFigure', completions)
        self.assertEqual(len(completions), 1168)
        milo = Ontology('src/pysumo/data/MILO.kif', lpath=self.tmpdir)
        atexit.unregister(milo.action_log.log_io.flush_write_queues)
        with open(milo.path) as f:
            milo_kif = parser.kifparse(f, milo)
        merged_asts = parser.astmerge((self.kif, milo_kif))
        self.indexabstractor.update_index(merged_asts)
        completions = self.indexabstractor.get_completions()
        self.assertIn('TwoDimensionalFigure', completions)
        self.assertIn('SubstringFn', completions)
        self.assertEqual(len(completions), 3228)
        milo.action_log.log_io.flush_write_queues()

indexTestSuit = unittest.makeSuite(indexTestCase, 'test')

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(indexTestSuit)
