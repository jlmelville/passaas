set -e

coverage run setup.py test && black --check ${MODULE}
