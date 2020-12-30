#!/bin/bash
set -e -x

docker run --rm -v $(PWD):/io quay.io/pypa/manylinux2010_x86_64 /io/scripts/build-wheels.sh
docker run --rm -v $(PWD):/io quay.io/pypa/manylinux2010_i686 linux32 /io/scripts/build-wheels.sh
