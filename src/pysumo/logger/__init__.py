""" The pySUMO logging interface.

This package contains 2 modules:

- infolog: A singleton called from the entry point to initialize the python logging framework and set the loglevel.
- actionlog: Stores a list of all write operations on the Ontology and provides undo and redo functionality.

"""
from os import environ

__all__ = ['infolog', 'actionlog']

CONFIG_PATH = '/'.join([environ['HOME'], '.pysumo'])
