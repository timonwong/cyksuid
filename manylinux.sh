#!/bin/bash
set -e -x

docker run --rm -v $(PWD):/io quay.io/pypa/manylinux1_x86_64 /io/scripts/build-wheels.sh
docker run --rm -v $(PWD):/io quay.io/pypa/manylinux1_i686 linux32 /io/scripts/build-wheels.sh
