import os
import shutil

from flask import current_app
import pytest
import webtest as wt


@pytest.fixture(scope="function")
def groups_response(testapp):
    return testapp.get("/api/groups")


class TestGetAllGroups:
    def test_status(self, groups_response):
        assert groups_response.status_int == 200

    def test_response_length(self, groups_response):
        assert len(groups_response.json) == 5

    def test_names(self, groups_response):
        assert [d["name"] for d in groups_response.json] == [
            "root",
            "daemon",
            "bin",
            "adm",
            "dialout",
        ]

    def test_gids(self, groups_response):
        assert [d["gid"] for d in groups_response.json] == [0, 1, 2, 4, 20]

    def test_members(self, groups_response):
        assert [d["members"] for d in groups_response.json] == [
            [],
            [],
            [],
            ["syslog", "james"],
            ["james"],
        ]
