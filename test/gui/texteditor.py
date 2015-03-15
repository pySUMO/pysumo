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
4. Choose Merge.kif
5. Collapse Line 288
6. Collapse Line 136
7. Collapse Line 134
8. Uncollapse Line 134
9. Uncollapse Line 288
10. Collapse all
11. Expand all
"""
if __name__ == "__main__":
    tmpdir = mkdtemp()
    pysumo.CONFIG_PATH = tmpdir
    MainWindow.main()
    shutil.rmtree(tmpdir, ignore_errors=True)

