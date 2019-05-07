"""
App Initialization.

Uses an extension of the single source versioning strategy #5 from:
https://packaging.python.org/guides/single-sourcing-package-version/
Version is taken from that in setup.py, which in turn looks in openapi.yaml
"""
import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("passaas").version
except Exception:  # pragma: no cover pylint: disable=broad-except
    __version__ = "unknown"
