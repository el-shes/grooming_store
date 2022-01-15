from flask import Flask
import unittest
from app import db
from service import procedure, breed


class CreateUserTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def test_create_and_get_by_id_correct_procedure(self):
        """
        Testing correct procedure creation and get procedure by id service
        """
        mock_procedure = procedure.create_procedure("Paint", 400, 60)
        found_procedure = procedure.get_procedure(mock_procedure.id)

        self.assertTrue(mock_procedure)
        self.assertTrue(found_procedure)
        self.assertEqual("Paint", mock_procedure.name)
        self.assertEqual(400, found_procedure.basic_price)
        self.assertEqual(60, found_procedure.duration)
        procedure.delete_procedure(mock_procedure.id)
        db.session.commit()

    def test_update_procedure(self):
        """
        Checks whether procedure is updated
        """
        procedure_to_update = procedure.create_procedure("Teeth treatment", 400, 20)
        info_for_procedure = {"name": "Ear treatment", "basic_price": 500, "duration": 30}
        result = procedure.update_procedure(procedure_to_update.id, info_for_procedure["name"],
                                            info_for_procedure["basic_price"], info_for_procedure["duration"])
        self.assertTrue(result)
        self.assertEqual(500, result.basic_price)
        procedure.delete_procedure(procedure_to_update.id)
        db.session.commit()

    def test_correct_compute_total_price_procedure(self):
        """
        Testing correct computing of total price of the procedure
        """
        mock_procedure = procedure.create_procedure("Test compute", 500, 30)
        mock_breed = breed.create_breed("Pug", 1.5, 2.5, "link")
        total_price = procedure.compute_total_procedure_price(mock_procedure.id, mock_breed.id)
        self.assertTrue(mock_procedure)
        self.assertTrue(mock_breed)
        self.assertTrue(total_price)
        self.assertEqual(1875, total_price)
        procedure.delete_procedure(mock_procedure.id)
        breed.delete_breed(mock_breed.id)
        db.session.commit()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()