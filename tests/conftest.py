"""Defines fixtures available to all tests."""
# pylint: disable=redefined-outer-name,too-few-public-methods,invalid-name
import os
import shutil

import pytest
import webtest as wt

from passaas.app import create_app
from passaas.config import TestConfig, Config

# These modules contain extra configuration for testing misconfigured apps and map to
# directories in the test folder. You could store them all in this file, but it leads
# to a large file that is hard to navigate.
pytest_plugins = ["bad_passwd_config", "bad_group_config"]


@pytest.yield_fixture(scope="function")
def app():
    """Application for the tests."""
    _app = create_app(TestConfig)

    ctx = _app.app.test_request_context()
    ctx.push()

    yield _app.app

    ctx.pop()


@pytest.fixture(scope="function")
def testapp(app):
    """Webtest app."""
    return wt.TestApp(app)


class PasswdUpdateConfig(TestConfig):
    """Configuration pointing to a passwd file intended to be updated between calls."""

    PASSWD_PATH = os.path.abspath(
        os.path.join(Config.PROJECT_ROOT, "tests", "test_data", "passwd4")
    )


@pytest.yield_fixture(scope="function")
def passwd_update_app():
    """Application with a passwd file intended to be updated."""
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
    """Webtest app with a passwd file intended to be updated."""
    return wt.TestApp(passwd_update_app)


# Groups


class GroupUpdateConfig(TestConfig):
    """Configuration pointing to a group file intended to be updated between calls."""

    GROUP_PATH = os.path.abspath(
        os.path.join(Config.PROJECT_ROOT, "tests", "test_data", "group4")
    )


@pytest.yield_fixture(scope="function")
def group_update_app():
    """Application with a passwd file intended to be updated."""
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
    """Webtest app with a group file intended to be updated."""
    return wt.TestApp(group_update_app)
