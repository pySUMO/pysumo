""" The PyUnit test framework for the parser. """

import unittest

from lib import parser

class wParseTestCase(unittest.TestCase):
    def test0Tokenize(self):
        line = '10495555 18 n 05 pusher 1 drug_peddler 0 peddler 1 drug_dealer 0 drug_trafficker 0 004 @ 10721470 n 0000 @ 09977660 n 0000 + 02302817 v 0301 + 02245555 v 0101 | an unlicensed dealer in illegal drugs &%Position+'
        position = parser._wtokenize(line, parser.Pos.noun).pop()
        assert position.sumo_concept == 'Position'
        assert position.suffix == '+'
        assert position.synset_offset == 2245555
        assert position.lex_filenum == 18
        assert position.ss_type == parser.SSType.noun
        assert position.synset == {1: ('pusher', None, 1), 2: ('drug_peddler', None, 0), 3: ('peddler', None, 1), 4: ('drug_dealer', None, 0), 5: ('drug_trafficker', None, 0)}
        assert position.ptr_list == [('@', parser.Pos.noun, 10721470, 0, 0), ('@', parser.Pos.noun, 9977660, 0, 0), ('+', parser.Pos.verb, 2302817, 3, 1), ('+', parser.Pos.verb, 2245555, 1, 1)]
        assert position.frames is None 
        assert position.gloss == 'an unlicensed dealer in illegal drugs'


    def test1Full(self):
        parser.wparse('data')


wParseSuit = unittest.makeSuite(wParseTestCase, 'test')

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(wParseSuit)
