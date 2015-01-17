""" The interface to the Natural Language Toolkit.

This module contains:

- WordNet: An interface to the WordNet online English lexical database.

"""

#from nltk.corpus import wordnet

class WordNet():
    """ An interface to locate and search for items in WordNet. Uses NLTK to
    search WordNet for information about terms in the Ontology, to find
    colloquial variations of term names and to find terms that are synonyms of
    a word.

    Methods:

    - locate_term: Locates a term in WordNet.
    - find_synonym: Finds possibly synonyms for a word.

    """

    def locate_term(self, term):
        """ Use the mapping from SUMO to WordNet to retrieve information about a term.

        Kwargs:

        - term: the term to locate

        Returns:

        - String

        """

    def find_synonym(self, word):
        """ Searches WordNet for possible synonyms for word.

        Returns:

        - String[]

        """
