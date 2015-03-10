""" Test case for the GraphWidget"""
from tempfile import mkdtemp
from pySUMOQt import MainWindow
import pysumo
import shutil

"""
Steps:
1. Open pySUMO
2. Open TextEditor
3. Open Merge.kif
4. Collapse Line 289
5. Collapse Line 137
6. Collapse Line 135
6. Uncollapse Line 135
7. Uncollapse Line 289
8. Collapse all
9. Expand all
"""
if __name__ == "__main__":
    tmpdir = mkdtemp()
    pysumo.CONFIG_PATH = tmpdir
    MainWindow.main()
    shutil.rmtree(tmpdir, ignore_errors=True)

