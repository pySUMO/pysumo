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
  4. Select instance on Variant selector
  5. Select a root node
  6. Select a depth (1)
  7. Open a new ontology to write temporary content to.
  8. Add a node "bla" in Graph Widget
  9. Add a node "bla2"
  10. Add a node "bla" (error)
  11. Add a relation instance between "bla" and "bla2" (error)
  12. Change scale
  13. Choose a valid selector (there was a messagebox)
  14. Add a relation instance between "bla" and "bla2"
  15. Undo
  16. Redo
"""
if __name__ == "__main__":
    tmpdir = mkdtemp()
    pysumo.CONFIG_PATH = tmpdir
    MainWindow.main()
    shutil.rmtree(tmpdir, ignore_errors=True)

