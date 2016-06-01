import unittest
import os
import datetime

from project import app, db
from project._config import basedir
from project.models import Task

TEST_DB = "test.db"


class APITest(unittest.TestCase):
    #####################
    ##setup and teadown##
    #####################

    def setUp(self):
        app.config["Testing"] = True
        app.config["Debug"] = False
        app.config["WTF_CSRF_ENABLED"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ####################
    ##helper functions##
    ####################

    def add_tasks(self):
        db.session.add(
            Task(
                name="Run in circle task",
                due_date=datetime.datetime.now(),
                poste_date=datetime.datetime.now(),
                prioraty=1,
                status=1,
                user_id=1
            )
        )
        db.session.commit()

        db.session.add(
            Task(
                name="Secound dummmy task",
                due_date=datetime.datetime.now(),
                poste_date=datetime.datetime.now(),
                prioraty=1,
                status=1,
                user_id=1
            )
        )

        db.session.commit()

    #########
    ##tests##
    #########

    def test_collection_returns_right_data(self):
        self.add_tasks()
        response = self.app.get("api/v1/tasks", follow_redirects=True)

        assert response.status_code is 200
        assert response.mimetype == "application/json"
        assert b"Run in circle task" in response.data
        assert b"Secound dummmy task" in response.data

    def test_collection_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get("api/v1/tasks/2", follow_redirects=True)

        assert response.status_code is 200
        assert response.mimetype == "application/json"
        assert b"Run in circle task" not in response.data
        assert b"Secound dummmy task" in response.data


if __name__ == '__main__':
    unittest.main()
