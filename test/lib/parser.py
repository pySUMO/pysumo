""" The PyUnit test framework for the parser. """

import unittest
import subprocess

from tempfile import mkdtemp
from shutil import rmtree
from pysumo import parser
from pysumo.syntaxcontroller import Ontology

class wParseTestCase(unittest.TestCase):
    def test0Tokenize(self):
        line = '10495555 18 n 05 pusher 1 drug_peddler 0 peddler 1 drug_dealer 0 drug_trafficker 0 004 @ 10721470 n 0000 @ 09977660 n 0000 + 02302817 v 0301 + 02245555 v 0101 | an unlicensed dealer in illegal drugs &%Position+'
        position = parser._wtokenize(line, parser.Pos.noun).pop()
        assert position.sumo_concept == 'Position'
        assert position.suffix == '+'
        assert position.synset_offset == 2245555
        assert position.lex_filenum == 18
        assert position.ss_type == parser.SSType.noun
        assert position.synset == [('pusher', None, 1), ('drug_peddler', None, 0), ('peddler', None, 1), ('drug_dealer', None, 0), ('drug_trafficker', None, 0)]
        assert position.ptr_list == [('@', parser.Pos.noun, 10721470, 0, 0), ('@', parser.Pos.noun, 9977660, 0, 0), ('+', parser.Pos.verb, 2302817, 3, 1), ('+', parser.Pos.verb, 2245555, 1, 1)]
        assert position.frames is None 
        assert position.gloss == 'an unlicensed dealer in illegal drugs'


    def test1Full(self):
        parser.wparse('data')


wParseSuit = unittest.makeSuite(wParseTestCase, 'test')

class kifParseSerilizeTest(unittest.TestCase):
    def test0ParseSerilize(self):
        tempd = mkdtemp()
        out1 = "/".join([tempd, "out1"])
        out2 = "/".join([tempd, "out2"])
        f = "data/Merge.kif"
        o = Ontology(f)
        with open(o.path) as f:
            a = parser.kifparse(f, o)
        self.assertNotEqual(a.children, [])
        with open(out1, 'w') as f:
            parser.kifserialize(a, o, f)
        with open(o.path) as f:
            a = parser.kifparse(f, o)
        with open(out2, 'w') as f:
            parser.kifserialize(a, o, f)
        ret = subprocess.call(["diff", out1, out2])
        rmtree(tempd)
        assert ret == 0

    def test1ParseGoverment(self):
        f = "data/Government.kif"
        o = Ontology(f)
        with open(o.path) as f:
            parser.kifparse(f, o)

kifParseSuit = unittest.makeSuite(kifParseSerilizeTest, 'test')

parseSuit = unittest.TestSuite((wParseSuit, kifParseSuit))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(parseSuit)
