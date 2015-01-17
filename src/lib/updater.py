""" Module which handles updating of Ontologies.
It use PycURL to check if any updates are avalible.
The URLs for the ontlogies are safe in the ontology
so the user can easy add an URL for a new ontlogy.
"""

import pycurl

def check_for_updates(ontology, function=None):
    """ Check if there are updates for ontology.  If an update is available,
    executes function.  Function receives the ontology as the first
    positional argument.

    Returns:

    - Boolean

    Raises:

    - HTTPError

    """
    return

def update(ontology, function=None):
    """ Checks for updates to ontology and if available downloads them. If the
    update succeeds, executes function after the download completes. Function
    receives the path to the downloaded ontology as the first positional
    argument, and ontology as the second.

    Raises:

    - HTTPError

    """
    return
