import unittest
import os

from project import db, app
from project._config import basedir

TEST_DB = "test.db"


class UnitTests(unittest.TestCase):
    ######################
    ##setup and teardown##
    ######################

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ###########
    ## tests ##
    ###########
    def test_error404(self):
        response = self.app.get("/this-page-does-not-exist")

        assert response.status_code == 404
        assert b"Oops something went wrong" in response.data


if __name__ == '__main__':
    unittest.main()
