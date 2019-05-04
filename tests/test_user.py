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


class TestBadPasswd:
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
