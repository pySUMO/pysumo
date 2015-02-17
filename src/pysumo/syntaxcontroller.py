""" Handles all write accesses to the Ontologies and kif files. The
SyntaxController's main purpose is to act as an intermediary between the user
and the Ontology.

This module contains:

- SyntaxController: The interface to the parser/serializer.

"""

from io import StringIO, BytesIO
from os import environ, listdir
from os.path import basename, isdir, join
from .logger import actionlog
from . import parser

def get_ontologies(packaged='/usr/local/share/pysumo', user='/'.join([environ['HOME'], '.pysumo'])):
    """ Returns a set of all ontologies provided by pysumo as well as local ontologies. """
    ret = set()
    if isdir(packaged):
        for f in listdir(packaged):
            if f.endswith(".kif"):
                ret.add(Ontology(join(packaged, f)))
    if isdir(user):
        for f in listdir(user):
            if f.endswith(".kif"):
                ret.add(Ontology(join(user, f)))
    return ret

class SyntaxController:
    """ The high-level class containing the interface to all parsing/serialization operations.
    All operations that can modify the Ontology or kif-file are passed through the SyntaxController.
    The SyntaxController acts as a moderator between user-side widgets and the low-level API
    ensuring that all requests are correct, that higher objects never gain direct access to
    internal objects and that all changes to the Ontology are atomic.

    Variables:

    - actionlog: The ActionLog for this object.

    Methods:

    - parse_partial: Checks a code block for syntax errors.
    - parse_add: Checks a code for correctness and adds it to the Ontology.
    - parse_graph: Modifies the current Ontology according to an AbstractGraph.
    - add_ontology: Adds an Ontology to the in-memory Ontology.
    - remove_ontology: Removes an Ontology from the in-memory Ontology.
    - serialize: Writes an Ontology out as Kif.

    """

    def __init__(self, index):
        """ Initializes the SyntaxController object. """
        self.index = index

    def parse_partial(self, code_block, ontology=None):
        """ Tells self.parser to check code_block for syntactical correctness.

        Arguments:

        - code_block: the partial code block that will be checked

        Raises:

        - ParseError

        """
        f = StringIO(code_block)
        ast = parser.kifparse(f, ontology)
        f.close()
        return ast

    def parse_add(self, code_block, ontology):
        """ Tells self.parser to check code_block for syntactical correctness and add it to the
        Ontology if it is correct.

        Arguments:

        - code_block: the code block that will be checked and added to the Ontology

        Raises:

        - ParseError

        """
        f = StringIO(code_block)
        parsed = parser.kifparse(f, ontology)
        # code_block needs to be the complete new kif file
        num = ontology.action_log.queue_log(BytesIO(code_block.encode()))
        newast = parser.astmerge((self.index.root, parsed))
        self.index.update_index(newast)
        ontology.action_log.ok_log_item(num)
        f.close()

    def parse_graph(self, graph):
        """ Tells self.parser to modify the current Ontology according to graph.

        Arguments:

        - graph: the AbstractGraph to check for modified nodes

        Raises:

        - ParseError

        """
        pass

    def add_ontology(self, ontology):
        """ Adds ontology to the current in-memory Ontology.

        Arguments:

        - ontology: the ontology that will be added

        Raises:

        - ParseError

        """
        with open(ontology.path) as f:
            newast = parser.kifparse(f, ontology, ast=self.index.root)
        # Not sure if reopening the file is faster than encoding to binary
        with open(ontology.path, 'r+b') as f:
            num = ontology.action_log.queue_log(BytesIO(f.read()))
        try:
            self.remove_ontology(ontology)
            newast = parser.astmerge((self.index.root, newast))
        except AttributeError:
            pass
        ontology.action_log.ok_log_item(num)
        newast.ontology = None
        self.index.update_index(newast)
        self.index.ontologies.add(ontology)

    def remove_ontology(self, ontology):
        """ Removes ontology from the current in-memory Ontology.

        Arguments:

        - ontology: the ontology that will be removed

        Raises:

        - NoSuchOntologyError

        """
        for c in list(self.index.root.children):
            if c.ontology == ontology:
                self.index.root.remove_child(c)
        self.index.update_index(self.index.root)
        self.index.ontologies.discard(ontology)

    def undo(self, ontology):
        """ Undoes the last action in ontology """
        kif = ontology.action_log.undo().getvalue().decode()
        self._update_asts(ontology, kif)

    def redo(self, ontology):
        """ Redoes the last action in ontology """
        kif = ontology.action_log.redo().getvalue().decode()
        self._update_asts(ontology, kif)

    def _update_asts(self, ontology, kif):
        ast = self.parse_partial(kif, ontology)
        self.remove_ontology(ontology)
        newast = parser.astmerge((self.index.root, ast))
        self.index.update_index(newast)

class Ontology:
    """ Contains basic information about a KIF file.  This class is used to
    maintain separation between different Ontology-files so the user can choose
    which are active and where each Ontology should be saved.

    Variables:

    - name: The name of the Ontology.
    - path: The location of the Ontology in the filesystem.
    - url: The URL from which the Ontology can be updated.
    - active: Whether or not the Ontology is currently loaded.

    """

    def __init__(self, path, name=None, url=None, lpath=None):
        """ Initializes an Ontology and instantiates variables. """
        if name is None:
            self.name = basename(path)
        else:
            self.name = name
        self.action_log = actionlog.ActionLog(self.name, lpath)
        self.path = path
        self.url = url
        self.active = False

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name
