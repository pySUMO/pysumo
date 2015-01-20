""" The pySUMO parsing module. It contains functions to parse and serialize
kif-files. It also handles the Ontology's data structure and parses the mapping
of SUMO terms to WordNet.


This module contains:

- AbstractSyntaxTree: The in-memory representation of an Ontology.
- Ontology: Contains basic information about an Ontology.

"""

import re

from os.path import basename
from enum import Enum

def tokenize(chars):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split(' ')

def cleanup(chars):
    chars = chars.rstrip()
    chars = chars[:chars.index(';')]
    return chars

def kifparse(ontology, graph=None, ast=None):
    """ Parse an ontology and return an AbstractSyntaxTree.

    Args:

    - ontology: the ontology to parse
    - graph: a modified graph of this ontology
    - ast: the AST of ontologies which are needed from this ontology

    Returns:

    - AbstractSyntaxTree

    """
    with open(ontology.path, 'r') as f:
        for line in f:
            line = cleanup(line)
            if line == "":
                break
            line = tokenize(line)



def astmerge(trees):
    """ Merge two Abstract Syntax Trees

    Args:

    - trees: a tuple of 2 AST objects

    Returns:

    - AbstractSyntaxTree

    """
    pass

def kifserialize(ast, ontology):
    """ Writes ontology to disk as kif. Parses ast and writes out all nodes
    that belong to ontology.

    Args:

    - ast: the Abstract Syntax Tree
    - ontology: The specific ontology with is written to disk

    Raises:

    - OSError

    """
    pass

def wparse(path):
    """ Parses the file containing the SUMO-WordNet mapping.

    Args:

    - path: The path to the SUMO-WordNet mapping files

    Returns:

    - Dictionary

    """
    mapping = dict()
    total, processed = 0, 0
    for pos in Pos:
        with open('%s/wordnet/sdata.%s' % (path, pos.name)) as data:
            for line in data:
                total += 1
                #Syntactical validation
                if re.match(r'^(\d{8}) (\d{2}) ([nvasr]) ([0-9a-zA-Z]{2})(?: (\S+ ([0-9a-zA-Z])))+ (\d{3})(?: ((\S{1,2}) \d{8} [nvasr] [0-9a-zA-Z]{4}))*(?: \d{2} (\+ \d{2} [0-9a-zA-Z]{2} )+)? ?\| .+ &%.+[\][@+:=]$', line):
                    items = _wtokenize(line.rstrip('\n'), pos)
                    processed += 1
                    for item in items:
                        try:
                            mapping[item.sumo_concept].add(item)
                        except KeyError:
                            mapping[item.sumo_concept] = {item}
    #TODO: Remove the fixed assertions/replace with dynamic assertions
    assert total == 117939, '%d lines were read, but %d lines should have been read' % (total, 117939)
    assert processed >= 117659 - 2000, 'processed %d, should have processed %d' % (processed, 117659)
    return mapping

def _wtokenize(line, pos):
    """ Returns all the tokens of a WordNet data line. """
    items = line.split(' ')
    # byte offset in current file
    synset_offset = int(items.pop(0))
    lex_filenum = int(items.pop(0))
    ss_type = SSType(items.pop(0))
    w_cnt = int(items.pop(0), 16)
    synset = dict()
    for i in range(1, w_cnt + 1):
        word = items.pop(0)
        if pos == Pos.adj and word[:-1] == ')':
            listy = word.split('(')
            syn_marker = listy.pop()[:-1]
            word = listy.pop()
        else:
            syn_marker = None
        lex_id = int(items.pop(0), 16)
        synset[i] = (word, syn_marker, lex_id)
    assert len(synset) == w_cnt, 'line %s has %d synsets, but should have %d' % (line, w_cnt, len(synset))
    p_cnt = int(items.pop(0))
    ptr_list = list()
    for i in range(0, p_cnt):
        pointer_symbol = items.pop(0)
        synset_offset = int(items.pop(0))
        p_pos = Pos(items.pop(0))
        so_ta = items.pop(0)
        source = int(so_ta[:2], 16)
        target = int(so_ta[2:], 16)
        ptr_list.append((pointer_symbol, p_pos, synset_offset, source, target))
    assert len(ptr_list) == p_cnt, 'line "%s" has %d pointers, but %s only contains %d' % (line, p_cnt, ptr_list, len(ptr_list))
    frames = None
    if ss_type == SSType.verb:
        f_cnt = int(items.pop(0))
        frames = set()
        for i in range(0, f_cnt):
            assert items.pop(0) == '+', "Frames not separated by a '+'"
            f_num = int(items.pop(0))
            w_num = int(items.pop(0), 16)
            frames.add((f_num, w_num))
        assert len(frames) == f_cnt, 'line %s has %d frames, but should have %d' % (line, f_cnt, len(frames))
    assert items.pop(0) == '|', "Missing '|' separator"
    assert len(items) != 0, 'No gloss or SUMO-term in %s' % line
    string = ' '.join(items)
    assert string != ''
    items = string.split('&%')
    assert len(items) >= 2, '"%s": %s should contain at least 2 items, but contains %d' % (line, items, len(items))
    gloss = items.pop(0).rstrip()
    sumo_concepts = set()
    while len(items) > 0:
        name = items.pop(0)
        suffix = name[-1:]
        name = name[:-1]
        sumo_concepts.add(SUMOConceptWordNetItem(name, suffix, synset_offset, lex_filenum, ss_type, synset, ptr_list, frames, gloss))
    return sumo_concepts

class SUMOConceptWordNetItem():
    """ The object returned from _wtokenize containing info on the SUMO-WordNet mapping. """
    def __init__(self, sumo_concept, suffix, synset_offset, lex_filenum,
                 ss_type, synset, ptr_list, frames, gloss):
        self.sumo_concept = sumo_concept
        self.suffix = suffix
        self.synset_offset = synset_offset
        self.lex_filenum = lex_filenum
        self.ss_type = ss_type
        self.synset = synset
        self.ptr_list = ptr_list
        self.frames = frames
        self.gloss = gloss

class Pos(Enum):
    noun = 'n'
    verb = 'v'
    adj = 'a'
    adv = 'r'

class SSType(Enum):
    noun = 'n'
    verb = 'v'
    adj = 'a'
    adv = 'r'
    adj_sat = 's'

class AbstractSyntaxTree():
    """ The AbstractSyntaxTree is a node in the abstract syntax tree. The
    abstract syntax tree is defined by a root node and its children. The
    AbstractSyntaxTree is the in-memory representation of the loaded Ontologies
    for internal purposes only and should never be passed outside of the lib.

    Variables:

    - parent: The parent node
    - children: A list of child nodes.
    - name: The name of the AbstractSyntaxTree object.
    - element_type: The type of the node element.
    - ontology: The Ontology object to which this node corresponds.
    - is_indexed: Whether or not this node is indexed.

    Methods:

    - get_children: Returns all child nodes.
    - add_child: Adds a child node.
    - remove_child: Removes a child node.

    """

    def __init__(self, ontology, parent=None):
        self.parent = parent
        self.children = []
        self.name = ''
        self.element_type = ''
        self.ontology = ontology
        self.is_indexed = False

    def get_children(self):
        """ Returns all children of self. """
        pass

    def add_child(self, entry):
        """ Adds entry as a child to self. """
        pass

    def remove_child(self, entry):
        """ Removes entry from the node's children. """
        pass

class Ontology():
    """ Contains basic information about a KIF file.  This class is used to
    maintain separation between different Ontology-files so the user can choose
    which are active and where each Ontology should be saved.

    Variables:

    - name: The name of the Ontology.
    - path: The location of the Ontology in the filesystem.
    - url: The URL from which the Ontology can be updated.
    - active: Whether or not the Ontology is currently loaded.

    """

    def __init__(self, path, name=None, url=None):
        """ Initializes an Ontology and instantiates variables. """
        if name is None:
            self.name = basename(path)
        else:
            self.name = name
        self.path = path
        self.url = url
        self.active = False
