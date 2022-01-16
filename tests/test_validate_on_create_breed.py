from flask import Flask
import unittest
from app import db
from service import breed


class CreateProcedureTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def test_validate_breed(self):
        """
        Validates correct breed inputs
        """
        mock_breed = {"name": "Pug", "fur_coefficient": 1.5, "size_coefficient": 3.0, "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertFalse(result)

    def test_validate_breed_wrong_name_input(self):
        """
        Validates breed wrong name input
        """
        mock_breed = {"name": "Corgi$", "fur_coefficient": 4.0, "size_coefficient": 3.5, "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("name" in result)
        self.assertEqual(result["name"], "Invalid symbol")

    def test_validate_breed_blank_name_input(self):
        """
        Validates breed name blank input
        """
        mock_breed = {"name": "", "fur_coefficient": 2.0, "size_coefficient": 4.5, "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("name" in result)
        self.assertEqual(result["name"], "Can't be blank")

    def test_validate_breed_name_already_exists(self):
        """
        Validates breed name that already exists
        """
        breed_1 = breed.create_breed("Cane Corso", 1.2, 7.7, "link")
        mock_breed = {"name": "Cane Corso", "fur_coefficient": 2.0, "size_coefficient": 4.5, "image_link": "link"}
        try:
            result = breed.validate_on_create(mock_breed)
            self.assertTrue(result)
            self.assertTrue("name" in result)
            self.assertEqual(result["name"], "Breed already exists")
        finally:
            breed.delete_breed(breed_1.id)

    def test_validate_fur_coefficient_blank_input(self):
        """
        Validates breed fur coefficient blank input
        """
        mock_breed = {"name": "Frenchie", "fur_coefficient": None, "size_coefficient": 4.5, "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("fur_coefficient" in result)
        self.assertEqual(result["fur_coefficient"], "Can't be blank")

    def test_validate_fur_coefficient_zero_input(self):
        """
        Validates breed fur coefficient zero input
        """
        mock_breed = {"name": "Akita", "fur_coefficient": 0, "size_coefficient": 5.2, "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("fur_coefficient" in result)
        self.assertEqual(result["fur_coefficient"], "Should be decimal")

    def test_validate_fur_coefficient_less_than_one_float_input(self):
        """
        Validates breed fur coefficient less than 1.0 input
        """
        mock_breed = {"name": "Shepherd", "fur_coefficient": 0.99, "size_coefficient": 3.4, "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("fur_coefficient" in result)
        self.assertEqual(result["fur_coefficient"], "Should be 1.00 or greater")

    def test_validate_fur_coefficient_long_float_input(self):
        """
        Validates breed fur coefficient less than 1.0 but rounded to 1.0 input
        """
        mock_breed = {"name": "Shepherd", "fur_coefficient": 0.9999999999, "size_coefficient": 3.4,
                      "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertFalse(result)

    def test_validate_fur_coefficient_integer_input(self):
        """
        Validates breed fur coefficient integer input
        """
        mock_breed = {"name": "Spaniel", "fur_coefficient": 4, "size_coefficient": 5.2, "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("fur_coefficient" in result)
        self.assertEqual(result["fur_coefficient"], "Should be decimal")

    def test_validate_fur_coefficient_string_input(self):
        """
        Validates breed fur coefficient string input
        """
        mock_breed = {"name": "Komondor", "fur_coefficient": "seven", "size_coefficient": 6.4, "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("fur_coefficient" in result)
        self.assertEqual(result["fur_coefficient"], "Should be decimal")

    def test_validate_size_coefficient_blank_input(self):
        """
        Validates breed size coefficient blank input
        """
        mock_breed = {"name": "Hound", "fur_coefficient": 1.7, "size_coefficient": None, "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("size_coefficient" in result)
        self.assertEqual(result["size_coefficient"], "Can't be blank")

    def test_validate_size_coefficient_zero_input(self):
        """
        Validates breed size coefficient zero input
        """
        mock_breed = {"name": "Dachshund", "fur_coefficient": 3.1, "size_coefficient": 0, "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("size_coefficient" in result)
        self.assertEqual(result["size_coefficient"], "Should be decimal")

    def test_validate_size_coefficient_less_than_one_float_input(self):
        """
        Validates breed size coefficient less than 1.0 input
        """
        mock_breed = {"name": "Spitz", "fur_coefficient": 3.3, "size_coefficient": 0.99, "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("size_coefficient" in result)
        self.assertEqual(result["size_coefficient"], "Should be 1.00 or greater")

    def test_validate_size_coefficient_long_float_input(self):
        """
        Validates breed size coefficient less than 1.0 but rounded to 1.0 input
        """
        mock_breed = {"name": "Shepherd", "fur_coefficient": 4.4, "size_coefficient": 0.9999999999,
                      "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertFalse(result)

    def test_validate_size_coefficient_integer_input(self):
        """
        Validates breed size coefficient integer input
        """
        mock_breed = {"name": "Shorthaired Pointer", "fur_coefficient": 1.5, "size_coefficient": 4,
                      "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("size_coefficient" in result)
        self.assertEqual(result["size_coefficient"], "Should be decimal")

    def test_validate_size_coefficient_string_input(self):
        """
        Validates breed size coefficient string input
        """
        mock_breed = {"name": "Labrador", "fur_coefficient": 3.2, "size_coefficient": "four", "image_link": "link"}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("size_coefficient" in result)
        self.assertEqual(result["size_coefficient"], "Should be decimal")

    def test_validate_breed_blank_image_link(self):
        """
        Validates breed image link blank input
        """
        mock_breed = {"name": "Mastiff", "fur_coefficient": 1.2, "size_coefficient": 4.8, "image_link": ""}
        result = breed.validate_on_create(mock_breed)
        self.assertTrue(result)
        self.assertTrue("image_link" in result)
        self.assertEqual(result["image_link"], "Can't be blank")

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
