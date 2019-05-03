set -e

pip install -r requirements.txt
pip install -r test-requirements.txt
pip install black

pip install coveralls

pip install -e .
