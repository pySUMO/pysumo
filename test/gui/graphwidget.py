""" Test case for the GraphWidget"""
from tempfile import mkdtemp
from pySUMOQt import MainWindow
import pysumo
import shutil

"""
Steps:
1. Open pySUMO
2. Open GraphWidget
3. Open Merge.kif
3. Select instance on Variant selector
4. Select a root node
5. Select a depth (1)
6. Open a new ontology to write temporary content to.
7. Add a node "bla" in Graph Widget
8. Add a node "bla2"
9. Add a node "bla" (error)
10. Add a relation instance between "bla" and "bla2" (error)
11. Change scale
12. Choose a valid selector (there was a messagebox)
13. Add a relation instance between "bla" and "bla2"
14. Undo
15. Redo
"""
if __name__ == "__main__":
    tmpdir = mkdtemp()
    pysumo.CONFIG_PATH = tmpdir
    MainWindow.main()
    shutil.rmtree(tmpdir, ignore_errors=True)

