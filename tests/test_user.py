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


@pytest.fixture(scope="function")
def user_exists_response(testapp):
    return testapp.get("/api/users/1")


class TestGetUserExists:
    def test_status(self, user_exists_response):
        assert user_exists_response.status_int == 200

    def test_response_length(self, user_exists_response):
        assert len(user_exists_response.json) == 6

    def test_name(self, user_exists_response):
        assert user_exists_response.json["name"] == "daemon"

    def test_uid(self, user_exists_response):
        assert user_exists_response.json["uid"] == 1

    def test_gid(self, user_exists_response):
        assert user_exists_response.json["gid"] == 1

    def test_comment(self, user_exists_response):
        assert user_exists_response.json["comment"] == "daemon"

    def test_home(self, user_exists_response):
        assert user_exists_response.json["home"] == "/usr/sbin"

    def test_shell(self, user_exists_response):
        assert user_exists_response.json["shell"] == "/usr/sbin/nologin"


@pytest.fixture(scope="function")
def user_does_not_exist_response(testapp):
    return testapp.get("/api/users/100", expect_errors=True)


class TestGetUserDoesNotExists:
    def test_status(self, user_does_not_exist_response):
        assert user_does_not_exist_response.status_int == 404


class TestQueryUser:
    """Test GET /users/query?name,uid,gid,comment,home,shell"""

    def test_query_name(self, testapp):
        response = testapp.get("/api/users/query?name=root")
        assert response.status_int == 200
        assert len(response.json) == 1
        assert response.json[0]["name"] == "root"

    def test_query_uid(self, testapp):
        response = testapp.get("/api/users/query?uid=1")
        assert response.status_int == 200
        assert len(response.json) == 1
        assert response.json[0]["uid"] == 1

    def test_query_gid(self, testapp):
        response = testapp.get("/api/users/query?gid=2")
        assert response.status_int == 200
        assert len(response.json) == 1
        assert response.json[0]["gid"] == 2

    def test_query_comment(self, testapp):
        response = testapp.get(r"/api/users/query?comment=Mailing%20List%20Manager")
        assert response.status_int == 200
        assert len(response.json) == 1
        assert response.json[0]["comment"] == "Mailing List Manager"

    def test_query_home(self, testapp):
        response = testapp.get(r"/api/users/query?home=%2Fbin")
        assert response.status_int == 200
        assert len(response.json) == 2
        assert response.json[0]["home"] == "/bin"

    def test_query_shell(self, testapp):
        response = testapp.get(r"/api/users/query?shell=%2Fusr%2Fsbin%2Fnologin")
        assert response.status_int == 200
        assert len(response.json) == 3
        assert list({e["shell"] for e in response.json}) == ["/usr/sbin/nologin"]

    def test_query_two_args(self, testapp):
        response = testapp.get(
            r"/api/users/query?home=%2Fbin&shell=%2Fusr%2Fsbin%2Fnologin"
        )
        assert response.status_int == 200
        assert len(response.json) == 1
        assert response.json[0]["home"] == "/bin"
        assert response.json[0]["shell"] == "/usr/sbin/nologin"

    def test_query_three_args(self, testapp):
        response = testapp.get(
            r"/api/users/query?gid=2&home=%2Fbin&shell=%2Fusr%2Fsbin%2Fnologin"
        )
        assert response.status_int == 200
        assert len(response.json) == 1
        assert response.json[0]["home"] == "/bin"
        assert response.json[0]["shell"] == "/usr/sbin/nologin"
        assert response.json[0]["gid"] == 2

    def test_query_empty_returns_everything(self, testapp):
        response = testapp.get("/api/users/query")
        assert response.status_int == 200
        assert len(response.json) == 5

    def test_unmatching_query_returns_404(self, testapp):
        response = testapp.get("/api/users/query?name=root&gid=1", expect_errors=True)
        assert response.status_int == 404


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

    def test_missing_passwd_return_500(self, test_missing_passwd_app):
        response = test_missing_passwd_app.get("/api/users", expect_errors=True)
        assert response.status_int == 500

    def test_malformed_passwd_too_few_return_500(
        self, test_malformed_passwd_too_few_elements_app
    ):
        response = test_malformed_passwd_too_few_elements_app.get(
            "/api/users", expect_errors=True
        )
        print(response)
        assert response.status_int == 500

    def test_malformed_passwd_too_many_return_500(
        self, test_malformed_passwd_too_many_elements_app
    ):
        response = test_malformed_passwd_too_many_elements_app.get(
            "/api/users", expect_errors=True
        )
        assert response.status_int == 500

    def test_malformed_passwd_bad_uid_return_500(
        self, test_malformed_passwd_bad_uid_app
    ):
        response = test_malformed_passwd_bad_uid_app.get(
            "/api/users", expect_errors=True
        )
        assert response.status_int == 500

    def test_malformed_passwd_bad_gid_return_500(
        self, test_malformed_passwd_bad_gid_app
    ):
        response = test_malformed_passwd_bad_gid_app.get(
            "/api/users", expect_errors=True
        )
        assert response.status_int == 500

    def test_empty_passwd_return_404(self, test_empty_passwd_app):
        response = test_empty_passwd_app.get("/api/users", expect_errors=True)
        assert response.status_int == 404
