import json
import flask_restful
from flask import Flask
import unittest
from app import db
from rest import user as user_rest
from rest import procedure as procedure_rest
from rest import master as master_rest


class RestProcedureTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)

        api = flask_restful.Api(self.app)
        api.add_resource(user_rest.User, '/user')
        api.add_resource(master_rest.Master, '/master')
        api.add_resource(procedure_rest.Procedure, '/procedure')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_procedure_post(self):
        """
        Checks correct procedure creation with correct input info
        """
        mock_procedure = json.dumps({"name": "Ear check", "basic_price": "400", "duration": "30"})
        response = self.client.post('/procedure', data=mock_procedure, headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)
        self.assertEqual("Ear check", response.json["name"])
        self.assertEqual(40000, response.json["basic_price"])
        self.assertEqual(30, response.json["duration"])

    def test_procedure_post_master_id(self):
        """
        Checks correct procedure creation with master_id
        """
        mock_procedure = json.dumps({"name": "Paint", "basic_price": "300", "duration": "30", "master_ids": "1"})
        response = self.client.post('/procedure', data=mock_procedure, headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)
        print(response.get_json())
        self.assertEqual("Paint", response.json["name"])
        self.assertEqual(30000, response.json["basic_price"])
        self.assertEqual(30, response.json["duration"])
        # self.assertEqual("1", response.json["master_ids"])

    def test_procedure_get_all(self):
        """
        Checks correct procedure get operation
        """
        mock_procedure1 = json.dumps({"name": "Paint", "basic_price": "300", "duration": "30"})
        mock_procedure2 = json.dumps({"name": "Ear clean", "basic_price": "200", "duration": "30"})
        response1 = self.client.post('/procedure', data=mock_procedure1, headers={"Content-Type": "application/json"})
        response2 = self.client.post('/procedure', data=mock_procedure2, headers={"Content-Type": "application/json"})
        get_response = self.client.get('/procedure')
        self.assertEqual(200, get_response.status_code)
        self.assertEqual("Paint", get_response.json[0]["name"])
        self.assertEqual(30000, get_response.json[0]["basic_price"])
        self.assertEqual(30, get_response.json[0]["duration"])
        self.assertEqual("Ear clean", get_response.json[1]["name"])
        self.assertEqual(20000, get_response.json[1]["basic_price"])
        self.assertEqual(30, get_response.json[1]["duration"])

    def test_procedure_put_by_procedure_id(self):
        pass

    def test_procedure_get_procedure_by_id(self):
        """

        """


    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
