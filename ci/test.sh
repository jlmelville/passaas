#!/bin/bash

set -e

if [[ "${COVERAGE}" == "true" ]]; then
    coverage run setup.py test && black --check ${MODULE}
else
    python setup.py test
fi
