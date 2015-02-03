""" The pySUMO parsing module. It contains functions to parse and serialize
kif-files. It also handles the Ontology's data structure and parses the mapping
of SUMO terms to WordNet.


This module contains:

- AbstractSyntaxTree: The in-memory representation of an Ontology.
- Ontology: Contains basic information about an Ontology.

"""

import re

from .logger import actionlog
from os.path import basename
from enum import Enum

def tokenize_docstring(chars, f):
    n = 0
    ret = []

    while  chars.count('"')%2 != 0 :
        n += 1
        line = f.readline()
        line = cleanup(line)
        chars = "".join([chars, line])
    chars = chars.split('"')
    while len(chars) > 1:
        c = tokenize(chars.pop(0))
        ret.extend(c)
        ret.append("".join(['"',chars.pop(0),'"']))
    ret.extend(tokenize(chars.pop(0)))
    return (ret, n)


def tokenize(chars):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def cleanup(chars):
    chars = chars.split(";")
    chars = chars[0]
    chars = chars.strip()
    return chars

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

def kifparse(ontology, graph=None, ast=None):
    """ Parse an ontology and return an AbstractSyntaxTree.

    Args:

    - ontology: the ontology to parse
    - graph: a modified graph of this ontology
    - ast: the AST of ontologies which are needed from this ontology

    Returns:

    - AbstractSyntaxTree

    """
    with open(ontology.path, 'r', errors='ignore') as f:
        docstring = False
        root = AbstractSyntaxTree(ontology)
        oldline = None
        linenumber = -1
        for i, line in enumerate(f):
            line = cleanup(line)
            if line == "":
                continue
            if '"' in line:
                line, n = tokenize_docstring(line, f)
                i += n
            else:
                line = tokenize(line)
            if oldline != None:
                line = oldline + line
                oldline = None
            if line[0] != '(':
                raise Exception("parse error in line",  i+1)
            if line.count('(') != line.count(')'):
                if linenumber == -1:
                    linenumber = i
                oldline = line
                continue
            if linenumber == -1:
                linenumber = i
            node = AbstractSyntaxTree(ontology, line=linenumber)
            parsed = node.parse(line)
            linenumber = -1

            if len(line) != parsed:
                print(line)
                print(len(line))
                print(parsed)
                raise Exception("parse error in line", i+1)
            root.add_child(node)
        return root

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
    with open(ontology.path, mode='w') as out:
        for child in ast.children:
            if child.ontology != ontology:
                continue
            line = "".join([str(child), '\n'])
            out.write(line)

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

    def __init__(self, ontology, parent=None, line=-1):
        if parent != None:
            self.parent = parent
        self.children = []
        self.name = ''
        self.element_type = ''
        self.ontology = ontology
        self.is_indexed = False
        self.line = line

    def __repr__(self):
        if len(self.children) == 0:
            return self.name
        out = " ".join(["(", self.name, ""])
        for child in self.children:
            out = "".join([out, str(child), " "])
        out = "".join([out, ")"])
        return out

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(repr(self))

    def parse(self, tokens):
        scip = 0
        for i, token in enumerate(tokens):
            if scip > 0:
                scip -= 1
                continue
            if token == '(':
                if self.name == '':
                    self.name = tokens[i+1]
                    scip += 1
                else:
                    child = AbstractSyntaxTree(self.ontology, parent=self, line=self.line)
                    scip += child.parse(tokens[i:])
                    scip -= 1
                    self.add_child(child)
            elif token == ')':
                return i+1
            else:
                child = AbstractSyntaxTree(self.ontology, parent=self, line=self.line)
                child.name = token
                self.add_child(child)

    def add_child(self, entry):
        """ Adds entry as a child to self. """
        entry.parent = self
        self.children.append(entry)

    def get_children(self):
        """ Returns all children of self. """
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
        self.action_log = actionlog.ActionLog(self.name)
        self.path = path
        self.url = url
        self.active = False

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)
