========
Examples
========

Read the Hamiltonian in the Wannier representation
==================================================

::

   from w90utils import io as w90io

   HR, Rvectors, Rweights = w90io.read_hr('wannier_hr.dat')
