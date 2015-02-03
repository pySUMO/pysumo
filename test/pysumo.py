""" The top-level TestSuite that calls the other suites. """

import os
import unittest


os.environ['PYTHONPATH'] = ':'.join([os.environ['PYTHONPATH'], os.getcwd()])

from test import parser
from test import wordnet
from test import indexabstractor

from test import actionlog


pySUMOSuit = unittest.TestSuite((parser.parseSuit, wordnet.WNTestSuit,
    indexabstractor.indexTestSuit, actionlog.actionLogSuit))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(pySUMOSuit)
