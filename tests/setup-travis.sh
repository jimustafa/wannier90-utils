#!/bin/bash
set -ex

cd "$HOME"
for version in 2.0.1 2.1.0; do
  curl http://wannier.org/code/wannier90-${version}.tar.gz | tar xz
  pushd wannier90-${version}
  touch make.sys make.inc
  F90=gfortran LIBS="-llapack -lblas" make
  popd
done
