""" Test case for the DocumentationWidget """
from tempfile import mkdtemp
from pySUMOQt import MainWindow
import pysumo
import shutil

"""
Steps:
1. Open pySUMO
2. Open Merge.kif
3. Open DocumentationWidget
3a. Switch to the Ontology tab in the DocumentationWidget
4. Type subrelation into the search field
4a. Press Enter
5. Open TextEditor
5a. Select Merge.kif in TextEditor
6. Press one of the links listed under "Merge"
7. Switch to the WordNet tab in the DocumentationWidget
8. Search for 'Object'
9. Search for 'Table'
"""
if __name__ == "__main__":
    tmpdir = mkdtemp()
    pysumo.CONFIG_PATH = tmpdir
    pysumo.PACKAGE_DATA = './data'
    MainWindow.main()
    shutil.rmtree(tmpdir, ignore_errors=True)

