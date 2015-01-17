""" The pySUMO logging interface.

This package contains 2 modules:

- infolog: A singleton called from the entry point to initialize the python logging framework and set the loglevel.
- actionlog: Stores a list of all write operations on the Ontology and provides undo and redo functionality.

"""

__all__ = ['infolog', 'actionlog']
