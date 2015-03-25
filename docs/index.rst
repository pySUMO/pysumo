.. pySUMO documentation master file, created by
   sphinx-quickstart on Thu Dec 18 16:01:48 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pysumo and pySUMOQt
===================

Introduction
============
This document introduces the Structure of our Ontology-editor pySUMO.

First, a short excursion to the "Model View Controller" design pattern is made.

Subsequently, our Class Diagram, which is structured according to the Model
View Controller (MVC) design.  Due to limited resources of paper size, the
class diagram is shown twice. Once as whole on page and one time on two pages
cut in middle to increase the readability.

Afterwards, several sequence diagrams which show a timeline of typical actions
are presented.

Furthermore, there are a couple of activity diagrams showcasing both a casual
pySUMO workflow as well as what pySUMO does in the background to support your
workflow.

Thereafter the individual classes are introduced in more detail. This is
followed up by a list of errors that pySUMO can throw and a list of external
libraries used to develop pySUMO.


Structure
=========
.. graphviz:: ./MVC.gv

The program is structured around the MVC-architecture. The partitioning into
Model, View and Controller makes modification of Program code easier and also
allows the lib to be used independently of the GUI.

For more information see

.. toctree::
  :maxdepth: 4

  mvc


UML Diagrams:
==================================



.. toctree::
  :maxdepth: 4

  sequence
  classdiagram

Detail: Modules
==================================

.. toctree::
   :maxdepth: 4


   pysumo
   pySUMOQt

Changes in Version 1.0
====================================

.. toctree::
   :maxdepth: 4

   Changes

Feature Request
===================================

.. toctree::
   :maxdepth: 4

   FeatureRequest
   test



Test Results
==================

.. toctree::
   :maxdepth: 4

   tests

For a more detailled view on our testing please visit `our github Page <http://pysumo.github.io/pysumo-htmlcov>`_

Errors
==========
+-------------------+--------------------------------------------+
|Errors             | Cause[s]                                   |
+===================+============================================+
|HTTPError          |An HTTP connection failed                   |
+-------------------+--------------------------------------------+
|IOError            |An IO operation failed                      |
+-------------------+--------------------------------------------+
|KeyError           |The specified key does not exist in the dict|
+-------------------+--------------------------------------------+
|NoSuchOntologyError|The specified Ontology does not exist       |
+-------------------+--------------------------------------------+
|NoSuchTermError    |The specified Term does not exist           |
+-------------------+--------------------------------------------+
|ParseError         |The specified Ontology is not valid         |
+-------------------+--------------------------------------------+

External Libraries
==================
+-----------+--------------------------------+
|PySide     |Python bindings for Qt          |
+-----------+--------------------------------+
|PyGraphviz |Python bindings for Graphviz    |
+-----------+--------------------------------+


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

