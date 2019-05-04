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


class TestUpdateGroupFile:
    """Test that changes to a group file are reflected in the response"""

    def test_response_reflects_change_to_passwd(self, test_group_update_app):
        # Establish that the file is in the expected initial state with 4 entries
        response = test_group_update_app.get("/api/groups")
        assert response.status_int == 200
        assert len(response.json) == 4

        # copy larger file over the original
        dest = current_app.config["GROUP_PATH"]
        dest_dir = os.path.dirname(dest)
        src = os.path.abspath(os.path.join(dest_dir, "group"))
        shutil.copyfile(src, dest)

        # Repeat request
        response = test_group_update_app.get("/api/groups")
        assert response.status_int == 200
        # there is now one more item in the result
        assert len(response.json) == 5

        # test_group_update restores original file


class TestBadGroup:
    """Tests for missing or malformed passwd files."""

    def test_missing_group_return_500(self, test_missing_group_app):
        response = test_missing_group_app.get("/api/groups", expect_errors=True)
        assert response.status_int == 500
