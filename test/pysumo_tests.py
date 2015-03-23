import os
import unittest
import pysumo

try:
    py_path = os.environ['PYTHONPATH']
except KeyError:
    py_path = ''

test_path = '/'.join([os.getcwd(), 'test'])
if test_path not in py_path.split(':'):
    os.environ['PYTHONPATH'] = ':'.join([py_path, test_path])

from lib import parser, wordnet, indexabstractor, actionlog, syntaxcontroller

pysumoSuit = unittest.TestSuite((parser.parseSuit, wordnet.WNTestSuit, indexabstractor.indexTestSuit, actionlog.actionLogSuit, syntaxcontroller.syntaxTestSuit))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(pysumoSuit)
