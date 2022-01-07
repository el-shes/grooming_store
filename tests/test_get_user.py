from flask import Flask
import unittest
from app import db
from service import user


class CreateUserTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def test_get_by_id_correct_user(self):
        """
        Testing correct user get service by id
        :return:
        """
        mock_user = user.create_user("Jane", "Eyer", "123", "CLIENT", "1231234567", )
        found_user = user.get_user(mock_user.id)
        self.assertTrue(found_user)
        self.assertEqual("Jane", found_user.first_name)
        self.assertEqual("Eyer", found_user.last_name)
        self.assertEqual("1231234567", found_user.phone)
        user.delete_user(found_user.id)
        db.session.commit()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()