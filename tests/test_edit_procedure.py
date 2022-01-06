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

    def test_validate_procedure(self):
        """
        Validates procedure information passed on update
        """
        procedure_1 = procedure.create_procedure("Haircut", 300, 30)
        info_for_procedure = {"name": "Hair", "basic_price": 400, "duration": 45}
        result = procedure.validate_on_update(info_for_procedure, procedure_1.id)
        self.assertFalse(result)
        procedure.delete_procedure(procedure_1.id)
        db.session.commit()

    def test_validate_name_procedure_exists(self):
        """
        Validates procedure with name that already exists
        """
        mock_procedure = procedure.create_procedure("Bath and paint", "400", "60")
        procedure_to_update = procedure.create_procedure("Nailtrim", "300", "30")
        info_for_procedure = {"name": "Bath and paint", "basic_price": "300", "duration": "30"}
        result = procedure.validate_on_update(info_for_procedure, procedure_to_update.id)
        self.assertTrue(result)
        self.assertTrue("name" in result)
        self.assertEqual(result["name"], "Procedure already exists")
        procedure.delete_procedure(procedure_to_update.id)
        db.session.commit()

    def test_validate_wrong_name_procedure(self):
        """
        Validates procedure with wrong name
        """
        procedure_to_update = procedure.create_procedure("Nailtrim", "300", "30")
        info_for_procedure = {"name": "##air", "basic_price": "300", "duration": "30"}
        result = procedure.validate_on_update(info_for_procedure, procedure_to_update.id)
        self.assertTrue(result)
        self.assertTrue("name" in result)
        self.assertEqual(result["name"], "Invalid symbol")
        procedure.delete_procedure(procedure_to_update.id)
        db.session.commit()

    def test_validate_blank_name_procedure(self):
        """
        Validates procedure with blank name input
        """
        procedure_to_update = procedure.create_procedure("Polish", "300", "30")
        info_for_procedure = {"name": "", "basic_price": "300", "duration": "30"}
        result = procedure.validate_on_update(info_for_procedure, procedure_to_update.id)
        self.assertTrue(result)
        self.assertTrue("name" in result)
        self.assertEqual(result["name"], "Can't be blank")
        procedure.delete_procedure(procedure_to_update.id)
        db.session.commit()

    def test_validate_blank_basic_price_procedure(self):
        """
        Validates procedure with blank basic_price input
        """
        procedure_to_update = procedure.create_procedure("Paw treatment", "400", "20")
        info_for_procedure = {"name": "Paw treatment", "basic_price": "", "duration": "20"}
        result = procedure.validate_on_update(info_for_procedure, procedure_to_update.id)
        self.assertTrue(result)
        self.assertTrue("basic_price" in result)
        self.assertEqual(result["basic_price"], "Can't be blank")
        procedure.delete_procedure(procedure_to_update.id)
        db.session.commit()

    def test_validate_non_numeric_basic_price_procedure(self):
        """
        Validates non-numeric basic_price input for procedure
        """
        procedure_to_update = procedure.create_procedure("Paw treatment", "400", "20")
        info_for_procedure = {"name": "Paw treatment", "basic_price": "two hundred", "duration": "20"}
        result = procedure.validate_on_update(info_for_procedure, procedure_to_update.id)
        self.assertTrue(result)
        self.assertTrue("basic_price" in result)
        self.assertEqual(result["basic_price"], "Should be a number")
        procedure.delete_procedure(procedure_to_update.id)
        db.session.commit()

    def test_validate_zero_basic_price_procedure(self):
        """
        Validates procedure with "0" basic_price input
        """
        procedure_to_update = procedure.create_procedure("Ear treatment", "400", "20")
        info_for_procedure = {"name": "Ear treatment", "basic_price": "0", "duration": "20"}
        result = procedure.validate_on_update(info_for_procedure, procedure_to_update.id)
        self.assertTrue(result)
        self.assertTrue("basic_price" in result)
        self.assertEqual(result["basic_price"], "Can't be zero")
        procedure.delete_procedure(procedure_to_update.id)
        db.session.commit()

    def test_validate_too_long_basic_price_procedure_input(self):
        """
        Validates too long basic_price input for procedure (bigger than 5 digits)
        """
        procedure_to_update = procedure.create_procedure("Teeth treatment", "400", "20")
        info_for_procedure = {"name": "Teeth treatment", "basic_price": "600344", "duration": "20"}
        result = procedure.validate_on_update(info_for_procedure, procedure_to_update.id)
        self.assertTrue(result)
        self.assertTrue("basic_price" in result)
        self.assertEqual(result["basic_price"], "Too long")
        procedure.delete_procedure(procedure_to_update.id)
        db.session.commit()

    def test_validate_blank_duration_procedure(self):
        """
        Validates procedure with blank duration input
        """
        procedure_to_update = procedure.create_procedure("Coloring", "400", "20")
        info_for_procedure = {"name": "Coloring", "basic_price": "400", "duration": ""}
        result = procedure.validate_on_update(info_for_procedure, procedure_to_update.id)
        self.assertTrue(result)
        self.assertTrue("duration" in result)
        self.assertEqual(result["duration"], "Can't be blank")
        procedure.delete_procedure(procedure_to_update.id)
        db.session.commit()

    def test_validate_non_numeric_duration_procedure(self):
        """
        Validates non-numeric duration input for procedure
        """
        procedure_to_update = procedure.create_procedure("Paw treatment", "400", "20")
        info_for_procedure = {"name": "Paw treatment", "basic_price": "400", "duration": "twenty"}
        result = procedure.validate_on_update(info_for_procedure, procedure_to_update.id)
        self.assertTrue(result)
        self.assertTrue("duration" in result)
        self.assertEqual(result["duration"], "Should be a number")
        procedure.delete_procedure(procedure_to_update.id)
        db.session.commit()

    def test_validate_zero_duration_procedure(self):
        """
        Validates procedure with "0" duration input
        """
        procedure_to_update = procedure.create_procedure("Coloring", 400, 20)
        info_for_procedure = {"name": "Coloring", "basic_price": 400, "duration": 0}
        result = procedure.validate_on_update(info_for_procedure, procedure_to_update.id)
        self.assertTrue(result)
        self.assertTrue("duration" in result)
        self.assertEqual(result["duration"], "Can't be zero")
        procedure.delete_procedure(procedure_to_update.id)
        db.session.commit()

    def test_validate_too_long_duration_procedure_input(self):
        """
        Validates too long duration input for procedure (bigger than 3 digits)
        """
        procedure_to_update = procedure.create_procedure("Teeth treatment", "400", "20")
        info_for_procedure = {"name": "Teeth treatment", "basic_price": "400", "duration": "3000"}
        result = procedure.validate_on_update(info_for_procedure, procedure_to_update.id)
        self.assertTrue(result)
        self.assertTrue("duration" in result)
        self.assertEqual(result["duration"], "Too long")
        procedure.delete_procedure(procedure_to_update.id)
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

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
