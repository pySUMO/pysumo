""" Handles all write accesses to the Ontologies and kif files. The
SyntaxController's main purpose is to act as an intermediary between the user
and the Ontology.

This module contains:

- SyntaxController: The interface to the parser/serializer.

"""

from io import StringIO, BytesIO
from os import listdir, fdopen, remove
from os.path import basename, isdir, join
from tempfile import mkstemp
from subprocess import Popen, PIPE, DEVNULL

import pysumo
from .logger import actionlog
from . import parser

def get_ontologies():
    """ Returns a set of all ontologies provided by pysumo as well as local ontologies. """
    ret = set()
    if isdir(pysumo.PACKAGE_DATA):
        for f in listdir(pysumo.PACKAGE_DATA):
            if f.endswith(".kif"):
                ret.add(Ontology(join(pysumo.PACKAGE_DATA, f)))
    if isdir(pysumo.CONFIG_PATH):
        for f in listdir(pysumo.CONFIG_PATH):
            if f.endswith(".kif"):
                ret.add(Ontology(join(pysumo.CONFIG_PATH, f)))
    return ret

class SyntaxController:
    """ The high-level class containing the interface to all parsing/serialization operations.
    All operations that can modify the Ontology or kif-file are passed through the SyntaxController.
    The SyntaxController acts as a moderator between user-side widgets and the low-level API
    ensuring that all requests are correct, that higher objects never gain direct access to
    internal objects and that all changes to the Ontology are atomic.

    Methods:

    - parse_partial: Checks a code block for syntax errors.
    - parse_add: Checks a code for correctness and adds it to the Ontology.
    - parse_graph: Modifies the current Ontology according to an AbstractGraph.
    - add_ontology: Adds an Ontology to the in-memory Ontology.
    - remove_ontology: Removes an Ontology from the in-memory Ontology.
    - serialize: Writes an Ontology out as Kif.

    """

    def __init__(self, index):
        """ Initializes the SyntaxController object. """
        self.index = index

    def parse_partial(self, code_block, ontology=None):
        """ Tells self.parser to check code_block for syntactical correctness.

        Arguments:

        - code_block: the partial code block that will be checked

        Raises:

        - ParseError

        """
        f = StringIO(code_block)
        ast = parser.kifparse(f, ontology)
        f.close()
        return ast

    def parse_patch(self, ontology, patch):
        """ Apply a patch to the last version of the ontology and parse this new version

        Arguments:

        - ontology: the ontlogy which is patched
        - patch: the patch to add to the ontology

        Raises:

        - ParseError

        """
        (tempfile, tempfilepath) = mkstemp(text=True)
        o = self.index.get_ontology_file(ontology)
        tempfile = fdopen(tempfile, 'wt')
        for l in o:
            print(l, end='', file=tempfile)
        tempfile.close()
        p = Popen(["patch", "-u", tempfilepath], stdin=PIPE, stdout=DEVNULL)
        p.communicate(patch.encode())
        with open(tempfilepath) as f:
            pos = f.tell()
            num = ontology.action_log.queue_log(BytesIO(f.read().encode()))
            f.seek(pos)
            newast = parser.kifparse(f, ontology, ast=self.index.root)
        try:
            self.remove_ontology(ontology)
            newast = parser.astmerge((self.index.root, newast))
        except AttributeError:
            pass
        newast.ontology = None
        self.index.update_index(newast)
        self.index.ontologies.add(ontology)
        ontology.action_log.ok_log_item(num)
        remove(tempfilepath)
        
    def add_ontology(self, ontology, newversion=None):
        """ Adds ontology to the current in-memory Ontology.

        Arguments:

        - ontology: the ontology that will be added
        - newversion: a string witch represent the new verison of the ontology

        Raises:

        - ParseError

        """

        if newversion == None:
            with open(ontology.path, errors='replace') as f:
                pos = f.tell()
                num = ontology.action_log.queue_log(BytesIO(f.read().encode()))
                f.seek(pos)
                newast = parser.kifparse(f, ontology, ast=self.index.root)
        else:
            num = ontology.action_log.queue_log(BytesIO(newversion.encode()))
            f = StringIO(newversion)
            newast = parser.kifparse(StringIO(newversion), ontology, ast=self.index.root)
        try:
            self.remove_ontology(ontology)
            newast = parser.astmerge((self.index.root, newast))
        except AttributeError:
            pass
        newast.ontology = None
        self.index.update_index(newast)
        self.index.ontologies.add(ontology)
        ontology.action_log.ok_log_item(num)

    def remove_ontology(self, ontology):
        """ Removes ontology from the current in-memory Ontology.

        Arguments:

        - ontology: the ontology that will be removed

        Raises:

        - NoSuchOntologyError

        """
        offset = 0
        for n, c in enumerate(list(self.index.root.children)):
            if c.ontology == ontology:
                self.index.root.children.pop(n - offset)
                offset = offset + 1
        self.index.update_index(self.index.root)
        self.index.ontologies.discard(ontology)

    def undo(self, ontology):
        """ Undoes the last action in ontology """
        kif = ontology.action_log.undo().getvalue().decode()
        self._update_asts(ontology, kif)

    def redo(self, ontology):
        """ Redoes the last action in ontology """
        kif = ontology.action_log.redo().getvalue().decode()
        self._update_asts(ontology, kif)

    def _update_asts(self, ontology, kif):
        ast = self.parse_partial(kif, ontology)
        self.remove_ontology(ontology)
        newast = parser.astmerge((self.index.root, ast))
        self.index.update_index(newast)

class Ontology:
    """ Contains basic information about a KIF file.  This class is used to
    maintain separation between different Ontology-files so the user can choose
    which are active and where each Ontology should be saved.

    Variables:

    - name: The name of the Ontology.
    - path: The location of the Ontology in the filesystem.
    - url: The URL from which the Ontology can be updated.
    - active: Whether or not the Ontology is currently loaded.

    """

    def __init__(self, path, name=None, url=None, lpath=None):
        """ Initializes an Ontology and instantiates variables. """
        if name is None:
            self.name = basename(path)
        else:
            self.name = name
        self.action_log = actionlog.ActionLog(self.name, lpath)
        with open(path, 'r+b') as f:
            self.action_log.current = BytesIO(f.read())
        self.path = path
        self.url = url
        self.active = False

    def save(self):
        """ Saves all pending changes in self to self.path. """
        with open(self.path, 'w+b') as f:
            f.write(self.action_log.current.getbuffer())

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name
