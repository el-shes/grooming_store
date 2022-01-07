import json
import flask_restful
from flask import Flask
import unittest
from app import db
from rest import user as user_rest
from rest import procedure as procedure_rest
from rest import master as master_rest
from service import procedure


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
        api.add_resource(procedure_rest.ProcedureById, '/procedure/<int:procedure_id>')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_procedure_post(self):
        """
        Checks correct procedure creation with correct input info
        """
        mock_procedure = json.dumps({"name": "Ear check", "basic_price": 400, "duration": 30})
        response = self.client.post('/procedure', data=mock_procedure, headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)
        self.assertEqual("Ear check", response.json["name"])
        self.assertEqual(400, response.json["basic_price"])
        self.assertEqual(30, response.json["duration"])

    def test_procedure_post_master_id(self):
        """
        Checks correct procedure creation with master_id
        """
        mock_procedure = json.dumps({"name": "Paint", "basic_price": 300, "duration": 30, "master_ids": "1"})
        response = self.client.post('/procedure', data=mock_procedure, headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)
        self.assertEqual("Paint", response.json["name"])
        self.assertEqual(300, response.json["basic_price"])
        self.assertEqual(30, response.json["duration"])
        # self.assertEqual("1", response.json["master_ids"])

    def test_procedure_get_all(self):
        """
        Checks correct procedure get all operation
        """
        mock_procedure1 = json.dumps({"name": "Paint", "basic_price": 300, "duration": 30})
        mock_procedure2 = json.dumps({"name": "Ear clean", "basic_price": 200, "duration": 30})
        self.client.post('/procedure', data=mock_procedure1, headers={"Content-Type": "application/json"})
        self.client.post('/procedure', data=mock_procedure2, headers={"Content-Type": "application/json"})
        get_response = self.client.get('/procedure')
        self.assertEqual(200, get_response.status_code)
        self.assertEqual("Paint", get_response.json[0]["name"])
        self.assertEqual(300, get_response.json[0]["basic_price"])
        self.assertEqual(30, get_response.json[0]["duration"])
        self.assertEqual("Ear clean", get_response.json[1]["name"])
        self.assertEqual(200, get_response.json[1]["basic_price"])
        self.assertEqual(30, get_response.json[1]["duration"])

    def test_procedure_put_by_procedure_id(self):
        """
        Testing correct procedure update
        """
        mock_procedure = json.dumps({"name": "Brushing", "basic_price": 200, "duration": 30})
        response = self.client.post('/procedure', data=mock_procedure, headers={"Content-Type": "application/json"})
        procedure_id = response.json["id"]
        info_to_update = json.dumps({"name": "Crushing", "basic_price": 300, "duration": 60})
        update_response = self.client.put(f'/procedure/{procedure_id}', data=info_to_update,
                                          headers={"Content-Type": "application/json"})
        self.assertEqual(200, update_response.status_code)
        self.assertEqual("Crushing", update_response.json["name"])
        self.assertEqual(300, update_response.json["basic_price"])
        self.assertEqual(60, update_response.json["duration"])

    def test_procedure_get_procedure_by_id(self):
        """
        Tests whether get response gets existing procedure by id
        """
        mock_procedure = json.dumps({"name": "Nail treatment", "basic_price": 150, "duration": 30})
        response = self.client.post('/procedure', data=mock_procedure, headers={"Content-Type": "application/json"})
        procedure_id = response.json["id"]
        get_response = self.client.get(f'/procedure/{procedure_id}')
        self.assertEqual(200, get_response.status_code)
        self.assertEqual("Nail treatment", get_response.json["name"])
        self.assertEqual(150, get_response.json["basic_price"])
        self.assertEqual(30, get_response.json["duration"])

    def test_procedure_delete(self):
        """
        Tests whether delete procedure operation deletes the procedure
        """
        mock_procedure = json.dumps({"name": "Tail treatment", "basic_price": 250, "duration": 30})
        response = self.client.post('/procedure', data=mock_procedure, headers={"Content-Type": "application/json"})
        procedure_id = response.json["id"]
        get_response = self.client.delete(f'/procedure/{procedure_id}')
        deleted_procedure_query = procedure.get_procedure(procedure_id)
        self.assertEqual(200, get_response.status_code)
        self.assertEqual(None, deleted_procedure_query)

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
