.. wannier90-utils documentation master file, created by
   sphinx-quickstart on Tue Nov 14 23:56:09 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============
wannier90-utils
===============

This package provides a library of functions for reading/writing and
manipulating the data associated with the `wannier90`_ code [1_]

.. toctree::
   :maxdepth: 1

   about
   install
   examples
   ./apidoc/w90utils


Quick Example
=============

Read the Hamiltonian in the Wannier representation
--------------------------------------------------

::

   from w90utils import io as w90io

   HR, Rvectors, Rweights = w90io.read_hr('wannier_hr.dat')


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _wannier90: http://wannier.org
.. _1: http://dx.doi.org/10.1016/j.cpc.2014.05.003
