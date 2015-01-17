""" The pySUMO parsing module. It contains functions to parse and serialize
kif-files. It also handles the Ontology's data structure and parses the mapping
of SUMO terms to WordNet.


This module contains:

- AbstractSyntaxTree: The in-memory representation of an Ontology.
- Ontology: Contains basic information about an Ontology.

"""

from os.path import basename

def kifparse(ontology, graph=None, ast=None):
    """ Parse an ontology and return an AbstractSyntaxTree.

    Args:

    - ontology: the ontology to parse
    - graph: a modified graph of this ontology
    - ast: the AST of ontologies which are needed from this ontology

    Returns:

    - AbstractSyntaxTree

    """
    pass

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

def wparse(mapping):
    """ Parses the file containing the SUMO-WordNet mapping.

    Args:

    - mapping: The file for the SUMO WordNet mapping

    Returns:

    - Dictionary

    """
    pass

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
