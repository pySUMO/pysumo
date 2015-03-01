""" The interface to WordNet.

This module contains:

- WordNet: An interface to the WordNet online English lexical database.

"""

import pysumo
from . import parser

class WordNet:
    """ An interface to locate and search for items in WordNet. Searches
    WordNet for information about terms in the Ontology, to find colloquial
    variations of term names and to find terms that are synonyms of a word.

    Methods:

    - locate_term: Locates a term in WordNet.
    - find_synonym: Finds possibly synonyms for a word.

    """

    def __init__(self):
        try:
            self.mapping = parser.wparse(pysumo.CONFIG_PATH)
        except FileNotFoundError:
            self.mapping = parser.wparse(pysumo.PACKAGE_DATA)


    def locate_term(self, term):
        """ Use the mapping from SUMO to WordNet to retrieve information about a term.

        Kwargs:

        - term: the term to locate

        Returns:

        - (name : String, type : SSType, gloss : String)[]

        """
        return [(x.synset[0][0], x.ss_type, x.gloss) for x in self.mapping[term]]

    def find_synonym(self, word):
        """ Searches WordNet for possible synonyms for word.

        Returns:

        - String[]

        """
        ret = set()
        w = word.replace(' ', '_')
        for key, value in self.mapping.items():
            for wn_item in value:
                if w in [x[0] for x in wn_item.synset]:
                    ret.add(key)
        return ret
