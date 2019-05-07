# pylint: disable=invalid-name

"""
Settings.

Based on: https://github.com/pypa/sampleproject/blob/master/setup.py
"""

import re
from os import path
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Version will be parsed (via regex) from the swagger yaml, so we only have
# to maintain it in one place.
version = "0.0.1"
version_pattern = re.compile(r"^\s*version: (.+)")
with open(path.join(here, "passaas", "openapi.yaml")) as f:
    for line in f:
        result = version_pattern.search(line)
        if result is not None:
            version = result.group(1)
            break

setup(
    name="passaas",
    version=version,
    description="A simple web service for readonly access to passwd and group info",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jlmelville/passaas",
    author="jlmelville@gmail.com",
    author_email="jlmelville@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["Flask", "connexion", "swagger-ui-bundle>=0.0.2"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "WebTest"],
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/jlmelville/passaas/issues",
        "Source": "https://github.com/jlmelville/passaas/",
    },
)
