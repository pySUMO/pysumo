""" This module abstracts all operations on the Ontology index.  It is used for
every read operation on the Ontology. It eases access to the Ontology and
protects the data structures from direct user access.

This module contains:

- IndexAbstractor: The interface to the Ontology index.
- AbstractGraph: An object containing selected graph nodes and relations.
- AbstractGraphNode: A node in a AbstractGraph
- DotGraph: A Graphical representation of an AbstractGraph with DOT

"""

import string

from .wordnet import WordNet

class IndexAbstractor():
    """ The IndexAbstractor provides a high-level index of the
    AbstractSyntaxTree.  Each Ontology is represented by a hashmap, the list of
    these hashmaps is the index.  Average access time is in O(n) where n is the
    number of loaded Ontologies.

    Variables:

    - root: The root AbstractSyntaxTree node.
    - ontologies: The list of currently active Ontologies.
    - index: The index of all terms in the currently active Ontology.
    - wordnet: A reference to the Object containing the SUMO-WordNet mapping.

    Methods:

    - init_wordnet: Initializes the WordNet mapping.
    - update_index: Updates the index.
    - search: Searches for a term in the Ontology.
    - get_graph: Creates an abstract graph containing a view of the Ontology.
    - wordnet_locate: Returns information about a term from WordNet.

    """

    def __init__(self):
        """ Initializes the IndexAbstractor object. """
        self.root = None
        self.ontologies = set()
        self.index = dict()
        self.wordnet = None

    def init_wordnet(self):
        """ Initializes the SUMO mapping to WordNet. """
        self.wordnet = WordNet()

    def update_index(self, ast):
        """ Updates the index with all new AST nodes in ast. """
        self.root = ast
        self._build_index()

    def _build_index(self):
        """ Builds an index for ontology. """
        for child in self.root.children:
            self.ontologies.add(child.ontology)
            key = normalize(child.children[0].name)
            asts = self.index.get(key, list())
            asts.append(child)
            self.index[key] = asts

    def search(self, term):
        """ Search for term in the in-memory Ontology. Returns all objects that
        match the search.

        Returns:

        - {Ontology : String[]}

        """
        term = normalize(term)
        ret = {x : list() for x in self.ontologies}
        for ast in self.index.get(term, []):
            ret[ast.ontology].append(repr(ast))
        return ret

    def _find_term(self, term):
        """ Returns the denormalized version of term. """
        term = normalize(term)
        try:
            return self.index[term][0].children[0].name
        except KeyError:
            pass
        raise KeyError('%s not in index.' % term)

    def get_graph(self, variant, root, depth):
        """ Returns a hierarchical view of the Ontology.

        Arguments:

        - variant: the hierarchical variant to return
        - root: the root node from which the graph will be created
        - depth: the maximum depth of the graph

        Returns:

        - AbstractGraph

        """

    def wordnet_locate(self, term):
        """ Use the mapping from SUMO to WordNet to retrieve information about a term.

        Arguments:

        - term: the term to locate

        Returns:

        - String[]

        Raises:

        - KeyError

        """
        term = self._find_term(term)
        try:
            results = self.wordnet.locate_term(term)
        except AttributeError:
            self.init_wordnet()
            results = self.wordnet.locate_term(term)
        return [' '.join([x[0], ''.join(['(', x[1].value, '):']), x[2]]) for x in results]

class DotGraph():
    """ A utility class that handles layouting AbstractGraph objects.  This
    class returns a layouted version of an AbstractGraph and provides a mapping
    between the image and nodes in the AbstractGraph.

    Variables:

    - graph: AbstractGraph

    Methods:

    - get_node_from_position: receives an xy coordinate and returns the node at that position
    - get_edge_from_position: receives an xy coordinate and returns the edge at that position
    - get_position_from_node: receives a node and returns its layouted position
    - get_pic: returns the layouted graph

    """

    def __init__(self, graph):
        """ Initializes the DotGraph and instantiates variables. """
        self.graph = graph

    def get_node_from_position(self, xcoord, ycoord):
        """ Returns the AbstractGraphNode nearest to the given x y coordinate. """

    def get_edge_from_position(self, xcoord, ycoord):
        """ Returns the edge nearest to the given x y coordinate. """

    def get_position_from_node(self, node):
        """ Returns the x y coordinate of the given node. """

    def get_pic(self):
        """ Returns a layouted version of self.graph. """

class AbstractGraph():
    """ An abstract representation of a subset of an Ontology as a collection
    of nodes and relations. This class can be used together with a DotGraph to
    create a graphical representation of an Ontology, or passed to the
    SyntaxController to modify the Ontology.

    Variables:

    - nodes: The list of graph nodes.
    - relations: An adjacency matrix of all the paths in the graph.

    """

    def __init__(self, variant, root, depth):
        """ Initializes the AbstractGraph and instantiates variables. """
        self.nodes = []
        self.relations = [[]]
        self._settings = (variant, root, depth)

class AbstractGraphNode():
    """ A node in an AbstractGraph. Contains information necessary to recreate
    an AbstractSyntaxTree from an AbstractGraph.

    Varibles:

    - name: The name of the AbstractGraphNode.

    """

    def __init__(self, name):
        """ Initializes an AbstractGraphNode and instantiates variables. """
        self.name = name


def normalize(term):
    """ Normalizes term to aid in searching. """
    for p in string.punctuation:
        term = term.replace(p, '')
    return term.lower().strip()
