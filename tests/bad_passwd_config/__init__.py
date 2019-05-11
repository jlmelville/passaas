"""Configuration for test apps with bad (missing/malformed) passwd files.

All of this originally lived in test/conftest.py, but that file was getting long and
confusing.

conftest.py imports the fixtures here using:

pytest_plugins = ["bad_passwd_config"]

Testing the web app with a particular configuration uses the following three items:

1. A Config class. This extends the TestConfig and overrides the usual passwd file with
one in tests/test_data. Example: MissingPasswdConfig
2. An app fixture. This uses the config to create a flask app. Everything before the
yield is setup, everything afterwards is cleanup. Example: missing_passwd_app
3. A test app fixture. This wraps the app created above into a Webtest app. Example:
test_missing_passwd_app

Tests that want to use that app then just specify the name of the fixture in the usual
pytest way, e.g. in test_user.py, tests that make use of a test_missing_passwd_app
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


class MissingPasswdConfig(TestConfig):
    """Configuration pointing to a missing passwd file."""

    # https://github.com/jarus/flask-testing/issues/21
    # and https://stackoverflow.com/a/28139033
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PASSWD_PATH = os.path.abspath(
        # this file purposely doesn't exist
        os.path.join(Config.PROJECT_ROOT, "tests", "test_data", "missing_passwd")
    )


@pytest.yield_fixture(scope="function")
def missing_passwd_app():
    """Application with a missing passwd file."""
    _app = create_app(MissingPasswdConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_missing_passwd_app(missing_passwd_app):
    """Webtest app with a missing passwd file."""
    return wt.TestApp(missing_passwd_app)


class MalformedPasswdTooFewElementsConfig(TestConfig):
    """Configuration for a malformed passwd file with too few elements in a line."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PASSWD_PATH = os.path.abspath(
        os.path.join(
            Config.PROJECT_ROOT, "tests", "test_data", "malformed_passwd_too_few"
        )
    )


@pytest.yield_fixture(scope="function")
def malformed_passwd_too_few_elements_app():
    """Application with a malformed passwd file."""
    _app = create_app(MalformedPasswdTooFewElementsConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_malformed_passwd_too_few_elements_app(malformed_passwd_too_few_elements_app):
    """Webtest app with a malformed passwd file."""
    return wt.TestApp(malformed_passwd_too_few_elements_app)


class MalformedPasswdTooManyElementsConfig(TestConfig):
    """Configuration for a malformed passwd file with too many elements in a line."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PASSWD_PATH = os.path.abspath(
        os.path.join(
            Config.PROJECT_ROOT, "tests", "test_data", "malformed_passwd_too_many"
        )
    )


@pytest.yield_fixture(scope="function")
def malformed_passwd_too_many_elements_app():
    """Application with a malformed passwd file with too many elements in a line."""
    _app = create_app(MalformedPasswdTooManyElementsConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_malformed_passwd_too_many_elements_app(malformed_passwd_too_many_elements_app):
    """Webtest app with a malformed passwd file with too many elements in a line."""
    return wt.TestApp(malformed_passwd_too_many_elements_app)


class MalformedPasswdBadUidConfig(TestConfig):
    """Configuration pointing to a malformed passwd file with a non-numeric uid."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PASSWD_PATH = os.path.abspath(
        os.path.join(
            Config.PROJECT_ROOT, "tests", "test_data", "malformed_passwd_bad_uid"
        )
    )


@pytest.yield_fixture(scope="function")
def malformed_passwd_bad_uid_app():
    """Application with a bad uid passwd file."""
    _app = create_app(MalformedPasswdBadUidConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_malformed_passwd_bad_uid_app(malformed_passwd_bad_uid_app):
    """Webtest app with a bad uid passwd file."""
    return wt.TestApp(malformed_passwd_bad_uid_app)


class MalformedPasswdBadGidConfig(TestConfig):
    """Configuration pointing to a malformed passwd file with a non-numeric gid."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PASSWD_PATH = os.path.abspath(
        os.path.join(
            Config.PROJECT_ROOT, "tests", "test_data", "malformed_passwd_bad_gid"
        )
    )


@pytest.yield_fixture(scope="function")
def malformed_passwd_bad_gid_app():
    """Application with a bad gid passwd file."""
    _app = create_app(MalformedPasswdBadGidConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_malformed_passwd_bad_gid_app(malformed_passwd_bad_gid_app):
    """Webtest app with a bad gid passwd file."""
    return wt.TestApp(malformed_passwd_bad_gid_app)


class EmptyPasswdConfig(TestConfig):
    """Configuration pointing to an empty passwd file."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PASSWD_PATH = os.path.abspath(
        os.path.join(Config.PROJECT_ROOT, "tests", "test_data", "empty_passwd")
    )


@pytest.yield_fixture(scope="function")
def empty_passwd_app():
    """Application with an empty passwd file."""
    _app = create_app(EmptyPasswdConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_empty_passwd_app(empty_passwd_app):
    """Webtest app with an empty passwd file."""
    return wt.TestApp(empty_passwd_app)
