import unittest
import os
from project._config import basedir
from project import db, app

TEST_DATABASE = "test.db"


class UitTests(unittest.TestCase):
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
        confirm = confirm or password

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

    def logout(self):
        return self.app.get("/logout", follow_redirects=True)

    def add_new_task(self):
        return self.app.post("/add/",
                             data=dict(
                                 name="new_task_name",
                                 due_date="12/12/2015",
                                 prioraty="1"
                             ),
                             follow_redirects=True

                             )

    ######################
    ##setup and teardown##
    ######################
    def setUp(self):
        app.config["Testing"] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, TEST_DATABASE)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #########
    ##tests##
    #########

    def test_can_create_new_task(self):
        self.register()
        self.login()
        response = self.add_new_task()

        assert b"New task has been added succsefully" in response.data

    def test_user_can_mark_as_complete_task(self):
        self.register()
        self.login()
        self.add_new_task()

        response = self.app.post("/complete/1", follow_redirects=True)

        assert b"Task has been marked as complete succsefully" in response.data

    def test_user_can_delete(self):
        self.register()
        self.login()
        self.add_new_task()

        response = self.app.get("/delete/1", follow_redirects=True)

        assert b"Task has been removed succsefully" in response.data

    def test_can_not_modify_that_does_not_belong_to_you(self):
        self.register()
        self.login()
        self.add_new_task()
        self.logout()

        username = "new_test_user"
        password = "new_secret_test_password"
        email = "new_email@mail.bg"

        self.register(username=username, email=email, password=password, confirm=password)
        self.login(username=username, password=password)

        response = self.app.get("/tasks", follow_redirects=True)

        assert b"Mark Complete" not in response.data
        assert b"Delete" not in response.data


# Task has been removed succsefully!
if __name__ == '__main__':
    unittest.main()
