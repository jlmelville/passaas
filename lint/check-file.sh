#!/bin/bash

show_help() {
cat << EOF
Usage: ${0##*/} [-hs] [FILE]
Check Python FILE and write result to standard output.

    -h          display this help and exit
    -s          stricter linting.
EOF
}

strict=0
OPTIND=1
while getopts hs opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        s)  strict=1
            ;;
        *)
            show_help >&2
            exit 1
            ;;
    esac
done
shift "$((OPTIND-1))"   # Discard the options and sentinel --

pylintrc="lint/.pylintrc"
if [[ ${strict} -eq 1 ]]; then
    pylintrc="lint/.pylintrc-strict"
fi

if [[ $# -ne 1 ]]; then
    show_help >&2
    exit 1;
fi

file=$1
venvdir="venv"

if [[ ! -e ${venvdir} ]]; then
    echo "Installing a virtual environment"
    python3 -m venv ${venvdir}
    source ${venvdir}/bin/activate
fi
if [[ -z ${VIRTUAL_ENV} ]]; then
    source ${venvdir}/bin/activate
fi

whichpylint=$(which pylint)
if [[ $? -ne 0 ]]; then
    ./install-linters.sh
fi

bandit -q -c lint/bandit.yml ${file}
pylint ${file} --rcfile ${pylintrc}
flake8 ${file} --config lint/.flake8
