#!/bin/bash

set -e

pip install -r requirements.txt
pip install -r test-requirements.txt

if [[ "${COVERAGE}" == "true" ]]; then
    # Only run black formatting check when checking coverage
    pip install coverage coveralls black
fi

pip install -e .
