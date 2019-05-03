from setuptools import find_packages, setup

setup(
    name="passaas",
    version="1.0",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["Flask", "connexion"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
