ui package
==========
This section describes the graphical user interface of pySUMO. It will list all
modules and classes which are necessary to connect the functionality of the
pySUMO's lib with the view and usability of a great editor. For details on this
concept see the section about MVC-Structure. Note that the core work is done by
Qt and the Qt Designer, so almost all classes will inherit a class designed by
Qt Designer and compiled by PySide.

.. uml::
    !include ./UML/ui/package_ui.iuml

Module contents
---------------

.. automodule:: ui
    :members:
    :undoc-members:
    :show-inheritance:


Subpackages
-----------

.. toctree::

    ui.Widget

Submodules
----------

ui.MainWindow module
--------------------

.. uml::
    !include ./UML/ui/MainWindow.iuml

|

.. automodule:: ui.MainWindow
    :members:
    :undoc-members:
    :show-inheritance:


ui.Settings module
------------------

.. uml::
    !include ./UML/ui/Settings.iuml

|

.. automodule:: ui.Settings
    :members:
    :undoc-members:
    :show-inheritance:
