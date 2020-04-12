#!/bin/bash
set -ex

WANNIER90_VERSIONS="2.0.1 2.1 3.0.0 3.1.0"

if [ -z "$WANNIER90_ROOT" ]; then
  WANNIER90_ROOT=$HOME/wannier90/
fi

mkdir -p $WANNIER90_ROOT/src/

pushd $WANNIER90_ROOT
for version in $WANNIER90_VERSIONS; do
  pushd $WANNIER90_ROOT/src/
  if [ ! -f "v${version}.tar.gz" ]; then
    wget https://github.com/wannier-developers/wannier90/archive/v${version}.tar.gz
  fi
  popd

  tar zxf ./src/v${version}.tar.gz

  pushd wannier90-${version}
  if [ "$version" == "2.0.1" ]; then
    # cp config/make.sys.gfort make.sys
    touch make.sys
    echo "F90=gfortran" >> make.sys
    echo "LIBS=-lblas -llapack" >> make.sys
  else
    # cp config/make.inc.gfort make.inc
    touch make.inc
    echo "F90=gfortran" >> make.inc
    echo "LIBS=-lblas -llapack" >> make.inc
  fi
  make
  popd
done
