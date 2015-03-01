""" The pySUMO library package. This package contains the core functionality of
pySUMO.  It not only provides the GUI with a feature-rich API, but also
validates input and keeps the Ontologies in a consistent state.
"""

from os import environ

CONFIG_PATH = '/'.join([environ['HOME'], '.pysumo'])

PACKAGE_DATA = '/usr/local/share/pysumo'
