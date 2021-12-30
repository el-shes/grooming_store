from flask import Flask
import unittest
from app import db
from service import procedure


class CreateProcedureTest(unittest.TestCase):
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
        Validates correct procedure info input
        """
        mock_procedure = {"name": "Trim", "basic_price": "300", "duration": "20"}
        result = procedure.validate_on_create(mock_procedure)
        self.assertFalse(result)

    def test_validate_procedure_wrong_name_input(self):
        """
        Validates wrong name procedure input
        """
        mock_procedure = {"name": "Bath#and$body", "basic_price": "800", "duration": "60"}
        result = procedure.validate_on_create(mock_procedure)
        self.assertTrue(result)
        self.assertTrue("name" in result)
        self.assertEqual(result["name"], "Invalid symbol")

    def test_validate_procedure_name_already_exists(self):
        """
        Validates procedure name exists
        """
        mock_procedure = {"name": "Bath and brush", "basic_price": "800", "duration": "60"}
        result = procedure.validate_on_create(mock_procedure)
        self.assertTrue(result)
        self.assertTrue("name" in result)
        self.assertEqual(result["name"], "Procedure already exists")

    def test_validate_procedure_blank_name_input(self):
        """
        Validates blank name procedure input
        """
        mock_procedure = {"name": "", "basic_price": "500", "duration": "40"}
        result = procedure.validate_on_create(mock_procedure)
        self.assertTrue(result)
        self.assertTrue("name" in result)
        self.assertEqual(result["name"], "Can't be blank")

    def test_validate_wrong_basic_price_input(self):
        """
        Validates wrong non-numeric basic price input
        """
        mock_procedure = {"name": "Nail painting", "basic_price": "five", "duration": "40"}
        result = procedure.validate_on_create(mock_procedure)
        self.assertTrue(result)
        self.assertTrue("basic_price" in result)
        self.assertEqual(result["basic_price"], "Should be a number")

    def test_validate_zero_basic_price_input(self):
        """
        Validates wrong non-numeric basic price input
        """
        mock_procedure = {"name": "Nail trimming", "basic_price": "0", "duration": "40"}
        result = procedure.validate_on_create(mock_procedure)
        self.assertTrue(result)
        self.assertTrue("basic_price" in result)
        self.assertEqual(result["basic_price"], "Can't be zero")

    def test_validate_basic_price_blank_input(self):
        """
        Validates blank basic price input
        """
        mock_procedure = {"name": "Haircut", "basic_price": "", "duration": "60"}
        result = procedure.validate_on_create(mock_procedure)
        self.assertTrue(result)
        self.assertTrue("basic_price" in result)
        self.assertEqual(result["basic_price"], "Can't be blank")

    def test_validate_basic_price_too_long_input(self):
        """
        Validates blank basic price input
        """
        mock_procedure = {"name": "Full package", "basic_price": "8000", "duration": "90"}
        result = procedure.validate_on_create(mock_procedure)
        self.assertTrue(result)
        self.assertTrue("basic_price" in result)
        self.assertEqual(result["basic_price"], "Too long")

    def test_validate_wrong_duration_input(self):
        """
        Validates wrong duration input
        """
        mock_procedure = {"name": "Ear cleaning", "basic_price": "200", "duration": "twenty"}
        result = procedure.validate_on_create(mock_procedure)
        self.assertTrue(result)
        self.assertTrue("duration" in result)
        self.assertEqual(result["duration"], "Should be a number")

    def test_validate_zero_duration_input(self):
        """
        Validates zero duration input
        """
        mock_procedure = {"name": "Teeth cleaning", "basic_price": "150", "duration": "0"}
        result = procedure.validate_on_create(mock_procedure)
        self.assertTrue(result)
        self.assertTrue("duration" in result)
        self.assertEqual(result["duration"], "Can't be zero")

    def test_validate_duration_blank_input(self):
        """
        Validates blank duration input
        """
        mock_procedure = {"name": "Teeth cleaning", "basic_price": "150", "duration": ""}
        result = procedure.validate_on_create(mock_procedure)
        self.assertTrue(result)
        self.assertTrue("duration" in result)
        self.assertEqual(result["duration"], "Can't be blank")

    def test_validate_duration_too_long_input(self):
        """
        Validates too long duration input
        """
        mock_procedure = {"name": "Teeth cleaning", "basic_price": "50", "duration": "6000"}
        result = procedure.validate_on_create(mock_procedure)
        self.assertTrue(result)
        self.assertTrue("duration" in result)
        self.assertEqual(result["duration"], "Too long")

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()