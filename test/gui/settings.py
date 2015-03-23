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
5. Open GraphWidget
6. Open DocumentationWidget
7. Open Hierarchy Widget
8. Open TextEdiorWidget

"""
if __name__ == "__main__":
    tmpdir = mkdtemp()
    pysumo.CONFIG_PATH = tmpdir
    MainWindow.main()
    MainWindow.main()
    shutil.rmtree(tmpdir, ignore_errors=True)

