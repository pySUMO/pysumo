""" Handles all write accesses to the Ontologies and kif files. The
SyntaxController's main purpose is to act as an intermediary between the user
and the Ontology.

This module contains:

- SyntaxController: The interface to the parser/serializer.

"""

from io import StringIO
from .logger import actionlog
from . import parser

class SyntaxController():
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

    def parse_partial(self, code_block):
        """ Tells self.parser to check code_block for syntactical correctness.

        Arguments:

        - code_block: the partial code block that will be checked

        Raises:

        - ParseError

        """
        f = StringIO(code_block)
        parser.kifparse(f, None)
        f.close()

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
        newast = parser.astmerge((self.index.root, parsed))
        self.index.update_index(newast)
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
        try:
            self.remove_ontology(ontology)
            newast = parser.astmerge((self.index.root, newast))
        except AttributeError:
            pass
        self.index.update_index(newast)

    def remove_ontology(self, ontology):
        """ Removes ontology from the current in-memory Ontology.

        Arguments:

        - ontology: the ontology that will be removed

        Raises:

        - NoSuchOntologyError

        """
        for c in self.index.root.children:
            if c.ontology == ontology:
                self.index.root.remove_child(c)
        self.index.update_index(self.index.root)


    def serialize(self, ontology, path=None):
        """ Serializes ontology to path. """
