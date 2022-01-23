import json
import flask_restful
from flask import Flask
import unittest
from app import db
from rest import breed as breed_rest
from service import breed


class RestBreedTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)

        api = flask_restful.Api(self.app)
        api.add_resource(breed_rest.Breed, '/breed')
        api.add_resource(breed_rest.BreedById, '/breed/<int:breed_id>')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_post_breed(self):
        """
        Testing post operation on breed creation
        """
        mock_breed = json.dumps({"name": "Papillon", "fur_coefficient": 3.7, "size_coefficient": 1.2,
                                 "image_link": "link"})
        response = self.client.post('/breed', data=mock_breed, headers={"Content-Type": "application/json"})
        try:
            self.assertEqual(200, response.status_code)
            self.assertEqual("Papillon", response.json["name"])
            self.assertEqual(3.7, response.json["fur_coefficient"])
            self.assertEqual(1.2, response.json["size_coefficient"])
        finally:
            breed.delete_breed(response.json["id"])

    def test_put_breeds(self):
        """
        Testing response on put by breed_id
        """
        breed_to_update = breed.create_breed("Dachshund", 1.5, 2.5, "image_link")
        mock_info_update = json.dumps({"name": "Dachshund", "fur_coefficient": 1.2, "size_coefficient": 2.0,
                                       "image_link": "link"})
        breed_id = breed_to_update.id
        update_response = self.client.put(f'/breed/{breed_id}', data=mock_info_update,
                                          headers={"Content-Type": "application/json"})
        try:
            self.assertEqual(200, update_response.status_code)
            self.assertEqual(1.2, update_response.json["fur_coefficient"])
            self.assertEqual(2.0, update_response.json["size_coefficient"])
        finally:
            breed.delete_breed(breed_id)

    def test_get_by_id_response(self):
        """
        Testing response on get breed by breed id
        """
        mock_breed = breed.create_breed("Bull Terrier", 1.0, 3.2, "image_link")
        breed_id = mock_breed.id
        get_response = self.client.get(f'breed/{breed_id}')
        try:
            self.assertEqual(200, get_response.status_code)
            self.assertEqual("Bull Terrier", get_response.json["name"])
            self.assertEqual(1.0, get_response.json["fur_coefficient"])
            self.assertEqual(3.2, get_response.json["size_coefficient"])
        finally:
            breed.delete_breed(breed_id)

    def test_delete_breed_response(self):
        """
        Testing response on delete breed operation
        """
        mock_breed = breed.create_breed("Bernhardiner", 4.1, 6.7, "image_link")
        breed_id = mock_breed.id
        delete_response = self.client.delete(f'breed/{breed_id}')
        deleted_breed_query = breed.get_breed(breed_id)
        self.assertEqual(200, delete_response.status_code)
        self.assertEqual(None, deleted_breed_query)

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
