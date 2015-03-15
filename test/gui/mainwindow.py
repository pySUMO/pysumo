'''
Created on Mar 10, 2015

@author: kent
'''
from tempfile import mkdtemp
import pysumo
from pySUMOQt import MainWindow
import shutil

"""
Steps:
1. Open pySUMO
2. Open a new Ontology named "Mondial"
3. Open a remote ontology named "Mondial" at location: http://sigmakee.cvs.sourceforge.net/viewvc/sigmakee/KBs/mondial.kif
4. Override the old version of the file Mondial by confirming the dialog.
5. Add Text Editor Widget
6. Add Documentation Widget
7. Add Graph Widget
8. Add Hierarchy Widget
9. Reorder Widgets
10. Make a print preview of the ontology "Mondial" from the Text Editor Widget
11. Make a print preview of the ontology "Mondial" from the Graph Widget
12. Quit pySUMO and save changes on file Mondial.kif
"""
if __name__ == "__main__":
    tmpdir = mkdtemp()
    pysumo.CONFIG_PATH = tmpdir
    MainWindow.main()
    MainWindow.main()
    shutil.rmtree(tmpdir, ignore_errors=True)
