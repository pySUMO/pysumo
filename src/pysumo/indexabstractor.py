""" This module abstracts all operations on the Ontology index.  It is used for
every read operation on the Ontology. It eases access to the Ontology and
protects the data structures from direct user access.

This module contains:

- IndexAbstractor: The interface to the Ontology index.
- AbstractGraph: An object containing selected graph nodes and relations.
- AbstractGraphNode: A node in a AbstractGraph
- DotGraph: A Graphical representation of an AbstractGraph with DOT

"""

from io import StringIO

import string

from pysumo.wordnet import WordNet

class IndexAbstractor:
    """ The IndexAbstractor provides a high-level index of the
    AbstractSyntaxTree.  Each Ontology is represented by a hashmap, the list of
    these hashmaps is the index.  Average access time is in O(n) where n is the
    number of loaded Ontologies.

    Variables:

    - root: The root AbstractSyntaxTree node.
    - ontologies: The list of currently active Ontologies.
    - index: The index of all terms in the currently active Ontologies.
    - wordnet: A reference to the Object containing the SUMO-WordNet mapping.

    Methods:

    - init_wordnet: Initializes the WordNet mapping.
    - update_index: Updates the index.
    - search: Searches for a term in the Ontology.
    - get_ontology_file: Return an in-memory file object for an Ontology.
    - get_completions: Return a list of possible completions for the current index.
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
        if self.wordnet is None:
            self.wordnet = WordNet()

    def update_index(self, ast):
        """ Updates the index with all new AST nodes in ast. """
        self.root = ast
        self.index = dict()
        self._build_index()

    def _build_index(self):
        """ Builds an index from self.root. """
        for child in self.root.children:
            self.ontologies.add(child.ontology)
            key = normalize(child.children[0].name)
            asts = self.index.get(key, list())
            asts.append(child)
            self.index[key] = asts

    def get_ontology_file(self, ontology):
        """ Returns an in-memory file object for the Kif representation of ontology. """
        if ontology in self.ontologies:
            ret = StringIO()
            ontology.action_log.current.seek(0)
            ret.write(ontology.action_log.current.read().decode('utf8'))
            ontology.action_log.current.seek(0)
            ret.seek(0)
            return ret

    def get_completions(self):
        """ Returns a list of possible completions for the currently loaded ontologies. """
        return [x[0].children[0].name for x in self.index.values()]

    def search(self, term):
        """ Search for term in the in-memory Ontology. Returns all objects that
        match the search.

        Returns:

        - {Ontology : (String, int)[]}

        """
        term = normalize(term)
        ret = {x: list() for x in self.ontologies}
        for ast in self.index.get(term, []):
            ret[ast.ontology].append((repr(ast), ast.line))
        return ret

    def _find_term(self, term):
        """ Returns the denormalized version of term. """
        term = normalize(term)
        try:
            return self.index[term][0].children[0].name
        except KeyError:
            pass
        raise KeyError('%s not in index.' % term)

    def get_graph(self, variant, major=2, minor=1, root=None, depth=None):
        """ Returns a hierarchical view of the Ontology.

        Arguments:

        - variant: The list of terms against which the resulting AbstractGraph matches.
        - major: The position of the parent element.
        - minor: The position of the child element.
        - root: The root node to which all other nodes are related.
        - depth: The recursion depth.

        Returns:

        - AbstractGraph

        Raises:

        - KeyError

        """
        if variant is None:
            return AbstractGraph(None, None, None, None, None, self.ontologies)
        else:
            var = [(x, normalize(y)) for x, y in variant]
            try:
                root = self._find_term(root)
            except AttributeError:
                pass
            return AbstractGraph(var, major, minor, root, depth, self.index)

    def wordnet_locate(self, term):
        """ Use the mapping from SUMO to WordNet to retrieve information about a term.

        Arguments:

        - term: the term to locate

        Returns:

        - String[]

        Raises:

        - KeyError

        """
        try:
            term = self._find_term(term)
            results = self.wordnet.locate_term(term)
        except KeyError:
            results = self._synonym_locate(normalize(term))
        except AttributeError:
            self.init_wordnet()
            results = self.wordnet.locate_term(term)
        return [' '.join([x[0], ''.join(['(', x[1].value, '):']), x[2]]) for x in results]

    def _synonym_locate(self, term):
        try:
            ret = list()
            synset = self.wordnet.find_synonym(term)
            for syn in synset:
                ret.extend(self.wordnet.locate_term(syn))
            return ret
        except AttributeError:
            self.init_wordnet()
            return self._synonym_locate(term)

class AbstractGraph:
    """ An abstract representation of a subset of an Ontology as a collection
    of nodes and relations.

    Variables:

    - nodes: The list of graph nodes.
    - relations: An adjacency matrix of all the paths in the graph.

    """

    def __init__(self, variant, major, minor, root, depth, info):
        """ Initializes the AbstractGraph and instantiates variables. """
        self.nodes = []
        self.relations = dict()
        self._settings = (variant, major, minor, root, depth)
        if variant is None:
            self._ontology_graph(info)
        else:
            self._relation_graph(info)
            if root is not None:
                self.nodes = sorted(self._filter_root(root, 0))
                self.nodes.append(root)
                self.relations = {
                    x: y for x, y in self.relations.items() if x in self.nodes}

    def _ontology_graph(self, ontologies):
        """ Produces an AbstractGraph of all the currently active ontologies. """
        self.nodes = [AbstractGraphNode(x) for x in ontologies]

    def _check_matches(self, node):
        """ Checks if node matches the variant. """
        try:
            for pos, val in self._settings[0]:
                if pos == 0 and node.name != val:
                    return False
                elif pos != 0 and node.children[pos - 1].name != val:
                    return False
            return True
        except IndexError:
            return False

    def _relation_graph(self, index):
        """ Produces an AbstractGraph containing all relations of type variant. """
        major_pos = self._settings[1]
        minor_pos = self._settings[2]
        node_set = set()
        for ast in index.values():
            for node in ast:
                if self._check_matches(node):
                    minor = node.children[minor_pos - 1].name
                    major = node.children[major_pos - 1].name
                    node_set.add(AbstractGraphNode(minor))
                    node_set.add(AbstractGraphNode(major))
                    relation = self.relations.get(major, set())
                    relation.add(minor)
                    self.relations[major] = relation
        self.nodes = sorted(node_set)

    def _filter_root(self, root, depth):
        """ Filters the AbstractGraph so only children of root are kept up to a maximum depth. """
        try:
            if depth >= self._settings[4]:
                return set()
        except TypeError:
            pass
        try:
            rel = set(self.relations[root])
        except KeyError:
            return set()
        for minor in self.relations[root]:
            try:
                rel = rel.union(self._filter_root(minor, depth + 1))
            except KeyError:
                rel.add(minor)
        return rel


class AbstractGraphNode:
    """ A node in an AbstractGraph. Contains information necessary to recreate
    an AbstractSyntaxTree from an AbstractGraph.

    Varibles:

    - name: The name of the AbstractGraphNode.

    """

    def __init__(self, name):
        """ Initializes an AbstractGraphNode and instantiates variables. """
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.name)


def normalize(term):
    """ Normalizes term to aid in searching. """
    for p in string.punctuation:
        term = term.replace(p, '')
    return term.lower().strip()
