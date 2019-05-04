"""Defines fixtures available to all tests."""
import os

import pytest
import webtest as wt

from passaas.app import create_app
from passaas.config import TestConfig, Config


@pytest.yield_fixture(scope="function")
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def testapp(app):
    """A Webtest app."""
    return wt.TestApp(app)


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
    """An application with a missing passwd file."""
    _app = create_app(MissingPasswdConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_missing_passwd_app(missing_passwd_app):
    """A Webtest app with a missing passwd file."""
    return wt.TestApp(missing_passwd_app)


class MalformedPasswdTooFewElementsConfig(TestConfig):
    """Configuration pointing to a malformed passwd file with too few elements in a line."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PASSWD_PATH = os.path.abspath(
        os.path.join(
            Config.PROJECT_ROOT, "tests", "test_data", "malformed_passwd_too_few"
        )
    )


@pytest.yield_fixture(scope="function")
def malformed_passwd_too_few_elements_app():
    """An application with a malformed passwd file."""
    _app = create_app(MalformedPasswdTooFewElementsConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_malformed_passwd_too_few_elements_app(malformed_passwd_too_few_elements_app):
    """A Webtest app with a malformed passwd file."""
    return wt.TestApp(malformed_passwd_too_few_elements_app)


class MalformedPasswdTooManyElementsConfig(TestConfig):
    """Configuration pointing to a malformed passwd file with too many elements in a line."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PASSWD_PATH = os.path.abspath(
        os.path.join(
            Config.PROJECT_ROOT, "tests", "test_data", "malformed_passwd_too_many"
        )
    )


@pytest.yield_fixture(scope="function")
def malformed_passwd_too_many_elements_app():
    """An application with a malformed passwd file with too many elements in a line."""
    _app = create_app(MalformedPasswdTooManyElementsConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_malformed_passwd_too_many_elements_app(malformed_passwd_too_many_elements_app):
    """A Webtest app with a malformed passwd file with too many elements in a line."""
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
    """An application with a bad uid passwd file."""
    _app = create_app(MalformedPasswdBadUidConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_malformed_passwd_bad_uid_app(malformed_passwd_bad_uid_app):
    """A Webtest app with a bad uid passwd file."""
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
    """An application with a bad gid passwd file."""
    _app = create_app(MalformedPasswdBadGidConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_malformed_passwd_bad_gid_app(malformed_passwd_bad_gid_app):
    """A Webtest app with a bad gid passwd file."""
    return wt.TestApp(malformed_passwd_bad_gid_app)
