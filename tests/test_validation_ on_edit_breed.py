from flask import Flask
import unittest
from app import db
from service import breed


class CreateUserTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def test_validate_breed_on_update(self):
        """
        Validates procedure information passed on update
        """
        breed_1 = breed.create_breed("Staff", 1.0, 3.2, "link")
        info_for_breed = {"name": "Terrier", "fur_coefficient": 1.5, "size_coefficient": 3.2, "image_link": "link"}
        result = breed.validate_on_update(info_for_breed, breed_1.id)
        self.assertFalse(result)
        breed.delete_breed(breed_1.id)
        db.session.commit()

    def test_validate_breed_wrong_name_update(self):
        """
        Validates breed wrong name on update
        """
        mock_breed = breed.create_breed("Rottweiler", 1.5, 3.2, "image_link")
        info_for_update = {"name": "Ro$$weiler", "fur_coefficient": 1.5, "size_coefficient": 3.2, "image_link": "link"}
        result = breed.validate_on_update(info_for_update, mock_breed.id)
        self.assertTrue(result)
        self.assertTrue("name" in result)
        self.assertEqual(result["name"], "Invalid symbol")
        breed.delete_breed(mock_breed.id)
        db.session.commit()

    def test_validate_breed_blank_name_update(self):
        """
        Validates breed with blank name on update
        """
        breed_to_update = breed.create_breed("Cane Corso", 1.2, 7.7, "image_link")
        info_for_update = {"name": "", "fur_coefficient": 1.2, "size_coefficient": 7.7, "image_link": "link"}
        result = breed.validate_on_update(info_for_update, breed_to_update.id)
        self.assertTrue(result)
        self.assertTrue("name" in result)
        self.assertEqual(result["name"], "Can't be blank")
        breed.delete_breed(breed_to_update.id)
        db.session.commit()

    def test_validate_breed_name_exists_on_update(self):
        """
        Validates breed with such name exists on update
        """
        mock_breed = breed.create_breed("Spaniel", 3.4, 2.5, "link")
        breed_to_update = breed.create_breed("Labrador Retriever", 2.5, 4.5, "link")
        info_for_update = {"name": "Spaniel", "fur_coefficient": 3.5, "size_coefficient": 4.5,
                           "image_link": "link"}
        result = breed.validate_on_update(info_for_update, breed_to_update.id)
        self.assertTrue(result)
        self.assertTrue("name" in result)
        self.assertEqual(result["name"], "Breed already exists")
        breed.delete_breed(breed_to_update.id)
        breed.delete_breed(mock_breed.id)
        db.session.commit()

    def test_validate_blank_fur_coefficient_update(self):
        """
        Validates blank fur coefficient update for breed
        """
        mock_breed = breed.create_breed("Paw friend", 2.2, 3.4, "image_link")
        info_for_update = {"name": "Paw friend", "fur_coefficient": None, "size_coefficient": 3.5, "image_link": "link"}
        result = breed.validate_on_update(info_for_update, mock_breed.id)
        self.assertTrue(result)
        self.assertTrue("fur_coefficient" in result)
        self.assertEqual(result["fur_coefficient"], "Can't be blank")
        breed.delete_breed(mock_breed.id)
        db.session.commit()

    def test_validate_fur_coefficient_zero_update(self):
        """
        Validates zero fur coefficient input for breed update
        """
        mock_breed = breed.create_breed("French Bulldog", 1.2, 2.4, "image_link")
        info_for_update = {"name": "French Bulldog", "fur_coefficient": 0, "size_coefficient": 2.5,
                           "image_link": "link"}
        result = breed.validate_on_update(info_for_update, mock_breed.id)
        self.assertTrue(result)
        self.assertTrue("fur_coefficient" in result)
        self.assertEqual(result["fur_coefficient"], "Should be decimal")
        breed.delete_breed(mock_breed.id)
        db.session.commit()

    def test_validate_fur_coefficient_less_than_one_float_update(self):
        """
        Validates breed fur coefficient less than 1.0 update
        """
        mock_breed = breed.create_breed("Shepherd", 2.5, 2.4, "image_link")
        info_for_update = {"name": "Shepherd", "fur_coefficient": 0.99, "size_coefficient": 2.5,
                           "image_link": "link"}
        result = breed.validate_on_update(info_for_update, mock_breed.id)
        self.assertTrue(result)
        self.assertTrue("fur_coefficient" in result)
        self.assertEqual(result["fur_coefficient"], "Should be 1.00 or greater")
        breed.delete_breed(mock_breed.id)
        db.session.commit()

    def test_validate_fur_coefficient_long_float_update(self):
        """
        Validates breed fur coefficient less than 1.0 but rounded to 1.0 update
        """
        mock_breed = breed.create_breed("Komondor", 7.0, 3.2, "image_link")
        info_for_update = {"name": "Komondor", "fur_coefficient": 0.9999999999, "size_coefficient": 2.5,
                           "image_link": "link"}
        result = breed.validate_on_update(info_for_update, mock_breed.id)
        self.assertFalse(result)
        breed.delete_breed(mock_breed.id)
        db.session.commit()

    def test_validate_fur_coefficient_string_update(self):
        """
        Validates breed fur coefficient string update
        """
        mock_breed = breed.create_breed("Komondor", 9.0, 3.2, "image_link")
        info_for_update = {"name": "Komondor", "fur_coefficient": "nine", "size_coefficient": 2.5,
                           "image_link": "link"}
        result = breed.validate_on_update(info_for_update, mock_breed.id)
        self.assertTrue(result)
        self.assertTrue("fur_coefficient" in result)
        self.assertEqual(result["fur_coefficient"], "Should be decimal")
        breed.delete_breed(mock_breed.id)
        db.session.commit()

    def test_validate_blank_size_coefficient_update(self):
        """
        Validates blank size_coefficient update for breed
        """
        mock_breed = breed.create_breed("Paw friend", 2.2, 3.4, "image_link")
        info_for_update = {"name": "Paw friend", "fur_coefficient": 2.2, "size_coefficient": None, "image_link": "link"}
        result = breed.validate_on_update(info_for_update, mock_breed.id)
        self.assertTrue(result)
        self.assertTrue("size_coefficient" in result)
        self.assertEqual(result["size_coefficient"], "Can't be blank")
        breed.delete_breed(mock_breed.id)
        db.session.commit()

    def test_validate_size_coefficient_zero_update(self):
        """
        Validates zero size_coefficient input for breed update
        """
        mock_breed = breed.create_breed("French Bulldog", 1.2, 2.4, "image_link")
        info_for_update = {"name": "French Bulldog", "fur_coefficient": 1.2, "size_coefficient": 0,
                           "image_link": "link"}
        result = breed.validate_on_update(info_for_update, mock_breed.id)
        self.assertTrue(result)
        self.assertTrue("size_coefficient" in result)
        self.assertEqual(result["size_coefficient"], "Should be decimal")
        breed.delete_breed(mock_breed.id)
        db.session.commit()

    def test_validate_size_coefficient_less_than_one_float_update(self):
        """
        Validates breed size_coefficient less than 1.0 update
        """
        mock_breed = breed.create_breed("Shepherd", 2.5, 2.4, "image_link")
        info_for_update = {"name": "Shepherd", "fur_coefficient": 2.5, "size_coefficient": 0.99,
                           "image_link": "link"}
        result = breed.validate_on_update(info_for_update, mock_breed.id)
        self.assertTrue(result)
        self.assertTrue("size_coefficient" in result)
        self.assertEqual(result["size_coefficient"], "Should be 1.00 or greater")
        breed.delete_breed(mock_breed.id)
        db.session.commit()

    def test_validate_size_coefficient_long_float_update(self):
        """
        Validates breed size_coefficient less than 1.0 but rounded to 1.0 update
        """
        mock_breed = breed.create_breed("Komondor", 7.0, 3.2, "image_link")
        info_for_update = {"name": "Komondor", "fur_coefficient": 6.5, "size_coefficient": 0.9999999999,
                           "image_link": "link"}
        result = breed.validate_on_update(info_for_update, mock_breed.id)
        self.assertFalse(result)
        breed.delete_breed(mock_breed.id)
        db.session.commit()

    def test_validate_size_coefficient_string_update(self):
        """
        Validates breed fur coefficient string update
        """
        mock_breed = breed.create_breed("Komondor", 9.0, 3.2, "image_link")
        info_for_update = {"name": "Komondor", "fur_coefficient": 5.5, "size_coefficient": "nine",
                           "image_link": "link"}
        result = breed.validate_on_update(info_for_update, mock_breed.id)
        self.assertTrue(result)
        self.assertTrue("size_coefficient" in result)
        self.assertEqual(result["size_coefficient"], "Should be decimal")
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
