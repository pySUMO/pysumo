""" Test case for the HierarchyWidget """
from tempfile import mkdtemp
from pySUMOQt import MainWindow
import pysumo
import shutil

"""
Steps:
1. Open pySUMO
2. Open HierarchyWidget
3. Open Merge.kif
4. Type instance into the Relation field
4a. Press Enter
5. Type unitofcurrency into the Node field
5a. Press Enter
6. Type subrelation into the Relation field
6a. Press Enter
7. Collapse all
8. Expand all
"""
if __name__ == "__main__":
    tmpdir = mkdtemp()
    pysumo.CONFIG_PATH = tmpdir
    MainWindow.main()
    shutil.rmtree(tmpdir, ignore_errors=True)

