""" This module involves all about the settings in the pySUMO GUI.

This module contains:

- WSettings: The settings of pySUMO's widgets.
- PluginManager: The manager for the plugin system in pySUMO.
- OptionDialog: The dialog that displays options of pySUMO.

"""

from PySide.QtCore import QSettings
from PySide.QtGui import QDialog

class WSettings(QSettings):
    """ This class represents the settings of the widgets in pySUMO's GUI.  The
    settings are stored in a local file for persistence and are loaded from
    there at init. """

    def __init__(self, widget):
        """ Initializes the widget's settings.

        Argument:

        - widget: The widget which owns the settings.

        """
        pass

class PluginManager():
    """ The PluginManager handles all loadabel plugins. At startup it loads all
    plugins and restores their settings from the persistence file.  It also
    manages unloading of plugins from the current application instance. The
    PluginManager also maintains the list of active plugins which is used on
    initialization of pySUMO to check which plugins should be loaded.
    """

    def __init__(self):
        """ Initializes the PluginManager. """
        self.plugins = []

    def get_plugins(self):
        """ Returns a list of the currently active plugins.

        Returns:

        - Widget[]

        """
        pass

    def add_plugin(self, path):
        """ Adds a plugin to the list of managed plugins.

        Argument:

        - path: The path where the plugin is located.

        Returns:

        - Boolean

        """
        pass

    def remove_plugin(self, name):
        """ Removes a plugin from the list of managed plugins.

        Argument:

        - name: The name of the plugin to remove.

        Returns:

        - Boolean

        """
        pass

class OptionDialog(QDialog):
    """ The option dialog is the displays and allows modification of settings
    for pySUMO. It displays options for the GUI, Widgets and library. The
    settings are organized by type and owner for ease of use. It also
    contains a plugin manager which enables loading and unloading of
    plugins.  The class also provides settings persistence by writing
    storing them in a file and reading from it on init.

    Attributes:

    - options: The options dictionary to manage in the option's dialog.

    Methods:

    - createView: Creates the view of the options dialog.
    - save: Saves the options.
    - load: Loads the options.

    """

    def __init__(self):
        """ Initializes the OptionDialog. """
        pass

    def createView(self):
        """ Initializes the view of the OptionDialog. """
        pass

    def save(self, path):
        """ Saves the settings to the given path.

        Arguments:

        - path: The path to which the settings will be written.

        Raises:

        - IOError

        """
        pass

    def load(self, path):
        """ Reads the settingns from the given path.

        Arguments:

        - path: The path from which the settings will be read.

        Raises:

        - IOError

        """
        pass
