import unittest
import os
from project._config import basedir
from project import db, app

TEST_DB = 'test.db'


class UniteTests(unittest.TestCase):
    __DEFAULT_PASSWORD = 'secret_password'
    __DEFAULT_USERNAME = 'test_user'
    __DEFAULT_EMAIL = 'test_user@mail.bg'

    ####################
    ##helper functions##
    ####################

    def register(self, username=None, email=None, password=None, confirm=None):
        username = username or self.__DEFAULT_USERNAME
        email = email or self.__DEFAULT_EMAIL
        password = password or self.__DEFAULT_PASSWORD
        confirm = password

        return self.app.post('/register/',
                             data=dict(
                                 name=username,
                                 password=password,
                                 confirm=confirm,
                                 email=email),
                             follow_redirects=True,
                             )

    def login(self, username=None, password=None):
        username = username or self.__DEFAULT_USERNAME
        password = password or self.__DEFAULT_PASSWORD

        return self.app.post(
            "/",
            data=dict(
                username=username,
                password=password
            ),
            follow_redirects=True
        )

    ######################
    ##setup and teardown##
    ######################

    def setUp(self):
        app.config["Testing"] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #########
    ##tests##
    #########

    def test_succsessful_register(self):
        response = self.register()

        assert b"Thanks for registrating!" in response.data

    def test_not_register_user_with_same_name(self):
        self.register()
        response = self.register()

        assert b"User with the same name or email adress already exists!" in response.data

    def test_non_register_user_can_not_loggin(self):
        response = self.login(username="invalid_username", password="invalid_password")

        assert b"Invalid user or password!" in response.data

    def test_register_user_can_login(self):
        self.register()
        response = self.login()

        assert b"Welcome" in response.data

    def test_loged_in_user_can_not_login_again(self):
        self.register()
        self.login()
        response = self.app.get('/', follow_redirects=True)
        assert b"You are allready loged in" in response.data

    def test_loged_user_can_log_out(self):
        self.register()
        self.login()
        response = self.app.get('/logout', follow_redirects=True)

        assert b"Goodbye" in response.data

    def test_non_loged_in_user_can_not_log_out(self):
        response = self.app.get('/logout', follow_redirects=True)

        assert b"You need to logg in first" in response.data

    def test_in_login_show_user_name(self):
        self.register(username="test_user")
        self.login(username="test_user")

        response = self.app.get("/tasks", follow_redirects=True)

        assert b"test_user" in response.data


if __name__ == '__main__':
    unittest.main()
