#!/bin/bash
set -e -x

docker run --rm -v $(PWD):/io quay.io/pypa/manylinux2010_x86_64:2020-01-31-046f791 /io/scripts/build-wheels.sh
docker run --rm -v $(PWD):/io quay.io/pypa/manylinux2010_i686:2020-01-31-046f791 linux32 /io/scripts/build-wheels.sh
