"""
Based on:
https://github.com/pypa/sampleproject/blob/master/setup.py
"""

from setuptools import find_packages, setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="passaas",
    version="1.0",
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
    install_requires=["Flask", "connexion"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "WebTest"],
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/jlmelville/passaas/issues",
        "Source": "https://github.com/jlmelville/passaas/",
    },
)
