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

    Methods:

    - search: searches for a term in the Ontology
    - get_graph: creates an abstract graph containing a view of the Ontology
    - wordnet_locate: returns information about a term from WordNet

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
            index = self.index.get(child.ontology, {child.ontology : dict()})
            key = normalize(child.children[0].name)
            asts = index.get(key, set())
            asts.add(child)
            index[key] = asts
            self.index[child.ontology] = index

    def search(self, term):
        """ Search for term in the in-memory Ontology. Returns all objects that
        match the search.

        Returns:

        - {Ontology : String[]}

        """
        term = normalize(term)
        ret = dict()
        for ontology, index in self.index.items():
            ret[ontology] = [repr(x) for x in index.get(term, [])]
        return ret

    def _find_term(self, term):
        """ Returns the denormalized version of term. """
        term = normalize(term)
        for index in self.index.values():
            try:
                return index[term].pop().children[0].name
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

        - String

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
