from flask import Flask
import unittest
from app import db
from service import master, user


class CreateProcedureTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def test_get_masters_by_ids(self):
        """
        Test getting masters by masters ids and returns lst of masters
        """
        user_1 = user.create_user("Nancy", "Joel", "123", "MASTER", "0123456789")
        user_2 = user.create_user("NancyA", "JoelA", "1234", "MASTER", "0123456788")
        master.create_master(user_1.id)
        master.create_master(user_2.id)
        try:
            result = master.get_all_from_list([user_1.id, user_2.id])
            self.assertTrue(result)
            self.assertEqual(2, len(result))
        finally:
            user.delete_user(user_1.id)
            user.delete_user(user_2.id)
            db.session.commit()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
