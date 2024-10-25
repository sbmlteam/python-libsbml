#!/bin/bash

git submodule update --init --remote

pushd libsbml_dependencies

# only checkout the expat submodule
git submodule update --init --remote expat

popd