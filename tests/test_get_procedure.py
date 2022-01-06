from flask import Flask
import unittest
from app import db
from service import procedure


class CreateUserTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def test_get_by_id_correct_procedure(self):
        """

        :return:
        """
        mock_procedure = procedure.create_procedure("Paint", 400, 60)
        found_procedure = procedure.get_procedure(mock_procedure.id)

        self.assertTrue(found_procedure)
        self.assertEqual(400, found_procedure["basic_price"])
        procedure.delete_procedure(mock_procedure.id)
        db.session.commit()


    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()