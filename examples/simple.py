#!/usr/bin/env python3

import sys
sys.path.append('../src')
from tempfile import mkdtemp

import pysumo
from pysumo import parser
from pysumo.indexabstractor import *
from pysumo.syntaxcontroller import Ontology

sumo = Ontology('../src/pysumo/data/Merge.kif', name='SUMO')
with open(sumo.path) as f:
    mergeKif = parser.kifparse(f, sumo)
index = IndexAbstractor()
index.update_index(mergeKif)

EntitySubclassGraph = index.get_graph([(0, 'subclass')], root='Entity')
print('In "subclass" relation with "Entity":')
print(EntitySubclassGraph.nodes)

BinaryPredicateInstanceGraph = index.get_graph([(0, 'instance')], root='BinaryPredicate')
print('\nIn "instance" relation with "BinaryPredicate":')
print(BinaryPredicateInstanceGraph.nodes)
