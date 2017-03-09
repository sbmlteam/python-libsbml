#!/bin/bash
echo -e " ... running twine to deploy ... "

echo -e "[distutils]
index-servers=
    pypi
    testpypi

[testpypi]
repository = https://testpypi.python.org/pypi

[pypi]
repository = https://pypi.python.org/pypi
" > pypirc

pip install twine
twine upload --config-file pypirc --skip-existing --repository testpypi --username "${PYPI_USERNAME}" --password "${PYPI_PASSWORD}" ${TRAVIS_BUILD_DIR}/wheelhouse/*
exit 0;
