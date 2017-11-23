#!/bin/bash
set -ex

cd "$HOME"
wget http://wannier.org/code/wannier90-2.0.1.tar.gz
tar zxvf wannier90-2.0.1.tar.gz
cd wannier90-2.0.1 && touch make.sys && F90=gfortran LIBS="-llapack -lblas" make
