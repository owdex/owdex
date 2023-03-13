import flask as f
import owdex.users
from owdex.usermanager import UserManager


def test_users(client):
    with client:
        create_response = client.post("/signup",
                                      data={
                                          "email": "test@test.test",
                                          "password": "test"
                                      })
        assert create_response.status_code == 200

        login_response = client.post("/login",
                                     data={
                                         "email": "test@test.test",
                                         "password": "test"
                                     })
        assert login_response.status_code == 200
        assert f.session["user"] == "test@test.test"

        protected_response = client.get("/protected")
        assert protected_response.status_code == 200
        assert f.session["user"] == "test@test.test"

        logout_response = client.get("/logout")
        assert logout_response.status_code == 200
        assert "user" not in f.session
