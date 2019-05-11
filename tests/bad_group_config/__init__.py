"""
Configuration for test apps with bad (missing/malformed) group files.

All of this originally lived in test/conftest.py, but that file was getting long and
confusing.

conftest.py imports the fixtures here using:

pytest_plugins = ["bad_group_config"]

Testing the web app with a particular configuration uses the following three items:

1. A Config class. This extends the TestConfig and overrides the usual group file with
one in tests/test_data. Example: MissingGroupConfig
2. An app fixture. This uses the config to create a flask app. Everything before the
yield is setup, everything afterwards is cleanup. Example: missing_group_app
3. A test app fixture. This wraps the app created above into a Webtest app. Example:
test_missing_group_app

Tests that want to use that app then just specify the name of the fixture in the usual
pytest way, e.g. in test_group.py, tests that make use of a test_missing_group_app
variable are using a server configured using the fixtures and class in the steps listed
above.
"""
# pylint: disable=redefined-outer-name,too-few-public-methods

import os
import shutil

import pytest
import webtest as wt

from passaas.app import create_app
from passaas.config import TestConfig, Config


class MissingGroupConfig(TestConfig):
    """Configuration pointing to a missing group file."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    GROUP_PATH = os.path.abspath(
        # this file purposely doesn't exist
        os.path.join(Config.PROJECT_ROOT, "tests", "test_data", "missing_group")
    )


@pytest.yield_fixture(scope="function")
def missing_group_app():
    """Application with a missing group file."""
    _app = create_app(MissingGroupConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_missing_group_app(missing_group_app):
    """Webtest app with a missing group file."""
    return wt.TestApp(missing_group_app)


class EmptyGroupConfig(TestConfig):
    """Configuration pointing to an empty group file."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    GROUP_PATH = os.path.abspath(
        os.path.join(Config.PROJECT_ROOT, "tests", "test_data", "empty_group")
    )


@pytest.yield_fixture(scope="function")
def empty_group_app():
    """Application with an empty passwd file."""
    _app = create_app(EmptyGroupConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_empty_group_app(empty_group_app):
    """Webtest app with an empty group file."""
    return wt.TestApp(empty_group_app)


class MalformedGroupTooFewElementsConfig(TestConfig):
    """Configuration for a malformed group file with too few elements in a line."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    GROUP_PATH = os.path.abspath(
        os.path.join(
            Config.PROJECT_ROOT, "tests", "test_data", "malformed_group_too_few"
        )
    )


@pytest.yield_fixture(scope="function")
def malformed_group_too_few_elements_app():
    """Application with a malformed group file that has too few elements in a line."""
    _app = create_app(MalformedGroupTooFewElementsConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_malformed_group_too_few_elements_app(malformed_group_too_few_elements_app):
    """Webtest app with a malformed group file that has too few elements in a line."""
    return wt.TestApp(malformed_group_too_few_elements_app)


class MalformedGroupTooManyElementsConfig(TestConfig):
    """Configuration for a malformed group file with too many elements in a line."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    GROUP_PATH = os.path.abspath(
        os.path.join(
            Config.PROJECT_ROOT, "tests", "test_data", "malformed_group_too_many"
        )
    )


@pytest.yield_fixture(scope="function")
def malformed_group_too_many_elements_app():
    """Application with a malformed group file with too many elements in a line."""
    _app = create_app(MalformedGroupTooManyElementsConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_malformed_group_too_many_elements_app(malformed_group_too_many_elements_app):
    """Webtest app with a malformed group file with too many elements in a line."""
    return wt.TestApp(malformed_group_too_many_elements_app)


class MalformedGroupBadGidConfig(TestConfig):
    """Configuration pointing to a malformed group file with a non-numeric gid."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    GROUP_PATH = os.path.abspath(
        os.path.join(
            Config.PROJECT_ROOT, "tests", "test_data", "malformed_group_bad_gid"
        )
    )


@pytest.yield_fixture(scope="function")
def malformed_group_bad_gid_app():
    """Application with a bad gid group file."""
    _app = create_app(MalformedGroupBadGidConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_malformed_group_bad_gid_app(malformed_group_bad_gid_app):
    """Webtest app with a bad gid group file."""
    return wt.TestApp(malformed_group_bad_gid_app)
