""" Module which handles updating of Ontologies.
It use PycURL to check if any updates are avalible.
The URLs for the ontlogies are safe in the ontology
so the user can easy add an URL for a new ontlogy.
"""

from io import BytesIO
from urllib.request import urlopen

def check_for_updates(ontology, function=lambda *a, **k: None):
    """ Check if there are updates for ontology.  If an update is available,
    executes function.  Function receives the new ontology file as the first
    positional argument.

    Returns:

    - Boolean

    Raises:

    - HTTPError

    """
    with urlopen(ontology.url) as f:
        b = BytesIO(f.read().decode('utf8', errors='replace').encode('utf8'))
    diff = ontology.action_log.log_io.diff(ontology.action_log.current, b).getvalue()
    if diff == b'':
        return False
    function(b)
    return True

def update(ontology, function=lambda *a, **k: None):
    """ Checks for updates to ontology and if available downloads them. If the
    update succeeds, executes function after the download completes. Function
    receives the path to the downloaded ontology as the first positional
    argument, and ontology as the second.

    Raises:

    - HTTPError

    """
    check_for_updates(ontology, function)
