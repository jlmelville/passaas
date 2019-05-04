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


@pytest.fixture(scope="function")
def group_exists_response(testapp):
    """reads the equivalent of: adm:x:4:syslog,james"""
    return testapp.get("/api/groups/4")


class TestGetUserExists:
    def test_status(self, group_exists_response):
        assert group_exists_response.status_int == 200

    def test_response_length(self, group_exists_response):
        assert len(group_exists_response.json) == 3

    def test_name(self, group_exists_response):
        assert group_exists_response.json["name"] == "adm"

    def test_gid(self, group_exists_response):
        assert group_exists_response.json["gid"] == 4

    def test_members(self, group_exists_response):
        assert group_exists_response.json["members"] == ["syslog", "james"]


class TestGetGroupDoesNotExist:
    def test_status(self, testapp):
        response = testapp.get("/api/groups/100", expect_errors=True)
        assert response.status_int == 404


class TestQueryGroup:
    """Test GET /groups/query?name,gid,member"""

    def test_query_name(self, testapp):
        response = testapp.get("/api/groups/query?name=root")
        assert response.status_int == 200
        assert len(response.json) == 1
        assert response.json[0]["name"] == "root"

    def test_query_gid(self, testapp):
        response = testapp.get("/api/groups/query?gid=2")
        assert response.status_int == 200
        assert len(response.json) == 1
        assert response.json[0]["gid"] == 2

    def test_query_member(self, testapp):
        response = testapp.get(r"/api/groups/query?member=james")
        assert response.status_int == 200
        assert len(response.json) == 2
        for result in response.json:
            assert "james" in result["members"]
        assert list(e["name"] for e in response.json) == ["adm", "dialout"]

    def test_query_repeat_members(self, testapp):
        response = testapp.get(r"/api/groups/query?member=james&member=syslog")
        assert response.status_int == 200
        assert len(response.json) == 1
        for result in response.json:
            for member in ["james", "syslog"]:
                assert member in result["members"]

    def test_query_repeat_members_comma_style(self, testapp):
        """Same as the previous test, but use a different format for repeated query"""
        response = testapp.get(r"/api/groups/query?member=james,syslog")
        assert response.status_int == 200
        assert len(response.json) == 1
        for result in response.json:
            for member in ["james", "syslog"]:
                assert member in result["members"]

    def test_query_two_args(self, testapp):
        response = testapp.get(r"/api/groups/query?name=dialout&gid=20")
        assert response.status_int == 200
        assert len(response.json) == 1
        assert response.json[0]["name"] == "dialout"
        assert response.json[0]["gid"] == 20

    def test_query_three_args(self, testapp):
        response = testapp.get(r"/api/groups/query?name=adm&gid=4&member=syslog")
        assert response.status_int == 200
        assert len(response.json) == 1
        assert response.json[0]["name"] == "adm"
        assert response.json[0]["gid"] == 4
        assert "syslog" in response.json[0]["members"]

    def test_query_empty_returns_everything(self, testapp):
        response = testapp.get("/api/groups/query")
        assert response.status_int == 200
        assert len(response.json) == 5

    def test_unmatching_query_returns_404(self, testapp):
        response = testapp.get("/api/groups/query?gid=42", expect_errors=True)
        assert response.status_int == 404

    def test_query_bad_parameter_returns_400(self, testapp):
        response = testapp.get(
            r"/api/groups/query?comment=Mailing%20List%20Manager", expect_errors=True
        )
        assert response.status_int == 400


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
    """Tests for missing or malformed group files."""

    @classmethod
    def setup_class(cls):
        cls.resource = "/api/groups"

    def test_missing_group_return_500(self, test_missing_group_app):
        response = test_missing_group_app.get(self.resource, expect_errors=True)
        assert response.status_int == 500

    def test_empty_group_return_404(self, test_empty_group_app):
        response = test_empty_group_app.get(self.resource, expect_errors=True)
        assert response.status_int == 404

    def test_malformed_group_too_few_return_500(
        self, test_malformed_group_too_few_elements_app
    ):
        response = test_malformed_group_too_few_elements_app.get(
            self.resource, expect_errors=True
        )
        assert response.status_int == 500

    def test_malformed_group_too_many_return_500(
        self, test_malformed_group_too_many_elements_app
    ):
        response = test_malformed_group_too_many_elements_app.get(
            self.resource, expect_errors=True
        )
        assert response.status_int == 500

    def test_malformed_group_bad_gid_return_500(self, test_malformed_group_bad_gid_app):
        response = test_malformed_group_bad_gid_app.get(
            self.resource, expect_errors=True
        )
        assert response.status_int == 500
