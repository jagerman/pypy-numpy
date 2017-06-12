#!/bin/bash

if [ -z "$1" ] || ! [[ "$1" = pypy* ]]; then
    echo "Error: usage: $0 pypy2-vX.Y.Z-linux64" >&2
    exit 1
fi
PYPY_NAME="$1"

set -e
rm -f *.whl

if ! [ -d "$PYPY_NAME" ]; then
    wget https://bitbucket.org/pypy/pypy/downloads/${PYPY_NAME}.tar.bz2
    tar xf ${PYPY_NAME}.tar.bz2
fi

docker run --volume="$PWD":/pypy-numpy --workdir=/pypy-numpy --rm ubuntu:trusty sh -c "
    set -e
    apt-get -qy update
    apt-get -qy install gcc g++ gfortran libblas-dev liblapack-dev ca-certificates
    export PATH=\"\${PATH}:/pypy-numpy/${PYPY_NAME}/bin\"
    pypy -m ensurepip
    pypy -m pip install wheel
    export NPY_NUM_BUILD_JOBS=4
    pypy -m pip wheel numpy
    pypy -m pip install numpy-*.whl
    pypy -m pip wheel scipy"
