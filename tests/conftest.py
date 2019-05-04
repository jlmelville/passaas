"""Defines fixtures available to all tests."""
import os
import shutil

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


class PasswdUpdateConfig(TestConfig):
    """Configuration pointing to a passwd file intended to be updated between calls."""

    PASSWD_PATH = os.path.abspath(
        os.path.join(Config.PROJECT_ROOT, "tests", "test_data", "passwd4")
    )


@pytest.yield_fixture(scope="function")
def passwd_update_app():
    """An application with a passwd file intended to be updated."""
    _app = create_app(PasswdUpdateConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    # Clean up after test
    dest = _app.app.config["PASSWD_PATH"]
    dest_dir = os.path.dirname(dest)
    src = os.path.abspath(os.path.join(dest_dir, "passwd4.orig"))
    shutil.copyfile(src, dest)

    ctx.pop()


@pytest.fixture(scope="function")
def test_passwd_update_app(passwd_update_app):
    """A Webtest app with a passwd file intended to be updated."""
    return wt.TestApp(passwd_update_app)


### Bad Passwords


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


class EmptyPasswdConfig(TestConfig):
    """Configuration pointing to an empty passwd file."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PASSWD_PATH = os.path.abspath(
        os.path.join(Config.PROJECT_ROOT, "tests", "test_data", "empty_passwd")
    )


@pytest.yield_fixture(scope="function")
def empty_passwd_app():
    """An application with an empty passwd file."""
    _app = create_app(EmptyPasswdConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def test_empty_passwd_app(empty_passwd_app):
    """A Webtest app with an empty passwd file."""
    return wt.TestApp(empty_passwd_app)


## Groups


class GroupUpdateConfig(TestConfig):
    """Configuration pointing to a group file intended to be updated between calls."""

    GROUP_PATH = os.path.abspath(
        os.path.join(Config.PROJECT_ROOT, "tests", "test_data", "group4")
    )


@pytest.yield_fixture(scope="function")
def group_update_app():
    """An application with a passwd file intended to be updated."""
    _app = create_app(GroupUpdateConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    # Clean up after test
    dest = _app.app.config["GROUP_PATH"]
    dest_dir = os.path.dirname(dest)
    src = os.path.abspath(os.path.join(dest_dir, "group4.orig"))
    shutil.copyfile(src, dest)

    ctx.pop()


@pytest.fixture(scope="function")
def test_group_update_app(group_update_app):
    """A Webtest app with a group file intended to be updated."""
    return wt.TestApp(group_update_app)
