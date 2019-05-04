import os
import shutil

from flask import current_app
import pytest
import webtest as wt


@pytest.fixture(scope="function")
def users_response(testapp):
    return testapp.get("/api/users")


class TestGetAllUsers:
    def test_status(self, users_response):
        assert users_response.status_int == 200

    def test_response_length(self, users_response):
        assert len(users_response.json) == 5

    def test_names(self, users_response):
        assert [d["name"] for d in users_response.json] == [
            "root",
            "daemon",
            "bin",
            "sync",
            "list",
        ]

    def test_uids(self, users_response):
        assert [d["uid"] for d in users_response.json] == [0, 1, 2, 4, 38]

    def test_gids(self, users_response):
        assert [d["gid"] for d in users_response.json] == [0, 1, 2, 65534, 38]

    def test_comments(self, users_response):
        assert [d["comment"] for d in users_response.json] == [
            "root",
            "daemon",
            "bin",
            "sync",
            "Mailing List Manager",
        ]

    def test_homes(self, users_response):
        assert [d["home"] for d in users_response.json] == [
            "/root",
            "/usr/sbin",
            "/bin",
            "/bin",
            "/var/list",
        ]

    def test_shells(self, users_response):
        assert [d["shell"] for d in users_response.json] == [
            "/bin/bash",
            "/usr/sbin/nologin",
            "/usr/sbin/nologin",
            "/bin/sync",
            "/usr/sbin/nologin",
        ]


class TestUpdatePasswdFile:
    """Test that changes to a passwd file are reflected in the response"""

    def test_response_reflects_change_to_passwd(self, test_passwd_update_app):
        # Establish that the file is in the expected initial state with 4 entries
        response = test_passwd_update_app.get("/api/users")
        assert response.status_int == 200
        assert len(response.json) == 4

        # copy larger file over the original
        dest = current_app.config["PASSWD_PATH"]
        dest_dir = os.path.dirname(dest)
        src = os.path.abspath(os.path.join(dest_dir, "passwd"))
        shutil.copyfile(src, dest)
        try:
            response = test_passwd_update_app.get("/api/users")
            assert response.status_int == 200
            # there is now one more item in the result
            assert len(response.json) == 5
        finally:
            # clean up by copying back over a copy of the original file
            src = os.path.abspath(os.path.join(dest_dir, "passwd4.orig"))
            shutil.copyfile(src, dest)


class TestBadPasswd:
    """Tests for missing or malformed passwd files."""

    def test_missing_passwd_returns500(self, test_missing_passwd_app):
        response = test_missing_passwd_app.get("/api/users", expect_errors=True)
        assert response.status_int == 500

    def test_malformed_passwd_too_few_returns500(
        self, test_malformed_passwd_too_few_elements_app
    ):
        response = test_malformed_passwd_too_few_elements_app.get(
            "/api/users", expect_errors=True
        )
        print(response)
        assert response.status_int == 500

    def test_malformed_passwd_too_many_returns500(
        self, test_malformed_passwd_too_many_elements_app
    ):
        response = test_malformed_passwd_too_many_elements_app.get(
            "/api/users", expect_errors=True
        )
        assert response.status_int == 500

    def test_malformed_passwd_bad_uid_returns500(
        self, test_malformed_passwd_bad_uid_app
    ):
        response = test_malformed_passwd_bad_uid_app.get(
            "/api/users", expect_errors=True
        )
        assert response.status_int == 500

    def test_malformed_passwd_bad_gid_returns500(
        self, test_malformed_passwd_bad_gid_app
    ):
        response = test_malformed_passwd_bad_gid_app.get(
            "/api/users", expect_errors=True
        )
        assert response.status_int == 500
