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

    def test_create_breed_service(self):
        """
        Testing breed is correctly created
        """
        mock_breed = breed.create_breed("American Eskimo", 3.3, 3.7,
                                        "https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11"
                                        "/13001724/American-Eskimo-Dog-On-White-01.jpg")
        try:
            self.assertTrue(mock_breed)
            self.assertEqual("American Eskimo", mock_breed.name)
            self.assertEqual(3.3, mock_breed.fur_coefficient)
            self.assertEqual(3.7, mock_breed.size_coefficient)
        finally:
            breed.delete_breed(mock_breed.id)
            db.session.commit()

    def test_update_breed_service(self):
        """
        Testing correct update on existing breed
        """
        mock_breed = breed.create_breed("Briard", 4.5, 4.1,
                                        "https://thumbs.dreamstime.com/b/%D0%B2%D0%B8%D0%B4-%D1%81%D0%B1%D0%BE%D0%BA"
                                        "%D1%83%D1%8B%D0%B9-9-%D0%BC%D0%B5%D1%81%D1%8F%D1%86%D0%B5%D0%B2-%D1%81%D0%BE"
                                        "%D0%B1%D0%B0%D0%BA%D0%B8-briard-%D1%81%D1%82%D0%B0%D1%80%D1%8B%D0%B9-%D1%81"
                                        "%D0%B8%D0%B4%D1%8F-12909720.jpg")
        info_to_update = {"name": "Briard", "fur_coefficient": 4.7, "size_coefficient": 4.5,
                          "image_link": "https://thumbs.dreamstime.com/b/%D0%B2%D0%B8%D0%B4-%D1%81%D0%B1%D0%BE%D0%BA"
                                        "%D1%83%D1%8B%D0%B9-9-%D0%BC%D0%B5%D1%81%D1%8F%D1%86%D0%B5%D0%B2-%D1%81%D0%BE"
                                        "%D0%B1%D0%B0%D0%BA%D0%B8-briard-%D1%81%D1%82%D0%B0%D1%80%D1%8B%D0%B9-%D1%81"
                                        "%D0%B8%D0%B4%D1%8F-12909720.jpg"}
        try:
            result = breed.update_breed(mock_breed.id, info_to_update["name"], info_to_update["fur_coefficient"],
                                        info_to_update["size_coefficient"], info_to_update["image_link"])
            self.assertTrue(result)
            self.assertEqual(4.7, result.fur_coefficient)
            self.assertEqual(4.5, result.size_coefficient)
        finally:
            breed.delete_breed(mock_breed.id)
            db.session.commit()

    def test_get_breed_by_id_service(self):
        """
        Testing correct breed is returned by id
        """
        mock_breed = breed.create_breed("Chilean Terrier", 1.2, 2.8,
                                        "https://www.whatsyourmuttdna.com/wp-content/uploads/Toy-Fox-Terrier.jpeg")
        try:
            found_breed = breed.get_breed(mock_breed.id)
            self.assertTrue(found_breed)
            self.assertEqual(mock_breed.name, found_breed.name)
            self.assertEqual(1.2, found_breed.fur_coefficient)
            self.assertEqual(2.8, found_breed.size_coefficient)
        finally:
            breed.delete_breed(mock_breed.id)
            db.session.commit()

    def test_get_all_breeds(self):
        """
        Testing that all breeds are returned by the service
        """
        mock_breed1 = breed.create_breed("French Spaniel", 5.1, 3.4, "image_link")
        mock_breed2 = breed.create_breed("Drentsche Patrijshond", 5.4, 2.5, "image_link")
        try:
            lst_of_found_breeds = breed.get_all()
            self.assertTrue(lst_of_found_breeds)
        finally:
            breed.delete_breed(mock_breed1.id)
            breed.delete_breed(mock_breed2.id)
            db.session.commit()

    def test_get_breed_by_name_service(self):
        """
        Testing that correct breed is returned in the query by name
        """
        mock_breed = breed.create_breed("Norfolk Terrier", 2.1, 1.5, "image_link")
        try:
            found_breed = breed.get_breed_by_name("Norfolk Terrier")
            self.assertTrue(found_breed)
            self.assertEqual(mock_breed.id, found_breed.id)
            self.assertEqual(mock_breed.name, found_breed.name)
            self.assertEqual(2.1, found_breed.fur_coefficient)
            self.assertEqual(1.5, found_breed.size_coefficient)
        finally:
            breed.delete_breed(mock_breed.id)
            db.session.commit()

    def test_delete_breed_service(self):
        mock_breed = breed.create_breed("Polish Greyhound", 1.2, 5.4, "image_link")
        breed.delete_breed(mock_breed.id)
        found_breed = breed.get_breed(mock_breed.id)
        self.assertFalse(found_breed)
        self.assertEqual(None, found_breed)

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
