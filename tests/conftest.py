"""Defines fixtures available to all tests."""

import pytest
import webtest as wt

from passaas.app import create_app
from passaas.config import TestConfig


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
