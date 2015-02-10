import os
import unittest

os.environ['PYTHONPATH'] = ':'.join([os.environ['PYTHONPATH'], os.getcwd() + '/test'])

from lib import parser, wordnet, indexabstractor, actionlog

pysumoSuit = unittest.TestSuite((parser.parseSuit, wordnet.WNTestSuit, indexabstractor.indexTestSuit, actionlog.actionLogSuit))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(pysumoSuit)
