#!/bin/bash

pip3 install -r linting-requirements.txt
pip3 uninstall --yes pycodestyle
pip3 install pycodestyle
pip3 uninstall --yes flake8
pip3 install flake8
