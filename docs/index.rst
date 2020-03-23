.. wannier90-utils documentation master file, created by
   sphinx-quickstart on Tue Nov 14 23:56:09 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============
wannier90-utils
===============

This package provides a library of functions for reading/writing and
manipulating the data associated with the `wannier90`_ code [1_].


Features
========

- Routines for reading/writing/manipulating a variety of files

  - manipulating WIN files (see :ref:`here <win>`)
  - parsing WOUT files (see :ref:`here <wout>`)
  - the ``nnkp`` file (see :ref:`here <nnkp>`)
  - the eigenvalues, overlap matrices, and projection matrices (see :ref:`here <basic>`)
  - output of ``postw90`` program, such as bandstructures (see :ref:`here <postw90>`)

- Utilities for computing the centers and spreads of Wannier functions (see :ref:`here <sprd>`)


Installation
============

To install the latest version of the wannier90-utils package, simply clone the repository and install using ``pip``.

::

   git clone https://github.com/jimustafa/wannier90-utils.git
   cd wannier90-utils && pip install .


Documentation
=============

.. toctree::
   :maxdepth: 2

   win
   wout
   nnkp
   basic
   sprd
   postw90
   examples


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _wannier90: http://wannier.org
.. _1: http://dx.doi.org/10.1016/j.cpc.2014.05.003
