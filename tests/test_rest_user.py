import json
import flask_restful
from flask import Flask
import unittest
from app import db
from rest import user as user_rest
from rest import master as master_rest
from rest import procedure as procedure_rest
from service import user as user_service, master, user


class RestUserTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)

        api = flask_restful.Api(self.app)
        api.add_resource(user_rest.User, '/user')
        api.add_resource(user_rest.UserById, '/user/<string:user_id>')
        api.add_resource(master_rest.Master, '/master')
        api.add_resource(procedure_rest.Procedure, '/procedure')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_user_post(self):
        """
        Checks correct user creation with correct input info
        """
        mock_user = json.dumps(
            {"first_name": "Becky", "last_name": "Bells", "phone": "1111111111", "password": "12345"})
        response = self.client.post('/user', data=mock_user, headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)
        self.assertEqual("Becky", response.json["first_name"])
        self.assertEqual("Bells", response.json["last_name"])
        self.assertEqual("1111111111", response.json["phone"])
        self.assertEqual("CLIENT", response.json["role"])

    def test_user_post_with_existing_phone(self):
        """
        Checks user creation with existing phone
        """
        user_service.create_user("Nancy", "Joel", "123", "MASTER", "1000000000")
        mock_user = json.dumps(
            {"first_name": "Becky", "last_name": "Bells", "phone": "1000000000", "password": "12345"})
        response = self.client.post('/user', data=mock_user, headers={"Content-Type": "application/json"})
        self.assertEqual(400, response.status_code)
        self.assertEqual("User with this phone number already exists",
                         json.loads(response.data.decode("utf-8"))["phone"])

    def test_user_post_without_password(self):
        """
        Checks user creation without password input
        """
        mock_user = json.dumps({"first_name": "Rick", "last_name": "Harding", "phone": "1111111111"})
        response = self.client.post('/user', data=mock_user, headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)

    def test_user_post_master_role(self):
        """
        Check user creation with master role
        """
        masters_amount_before = master.get_all()
        mock_user = json.dumps({"first_name": "Nancy", "last_name": "Drew", "role": "MASTER", "phone": "1111111111"})
        response = self.client.post('/user', data=mock_user, headers={"Content-Type": "application/json"})
        masters_amount_after = master.get_all()
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(masters_amount_before) + 1, len(masters_amount_after))
        self.assertEqual("MASTER", response.json["role"])

    def test_user_get_all_users(self):
        """
        Test whether get response returns all created users
        """
        mock_user = json.dumps(
            {"first_name": "Becky", "last_name": "Bells", "phone": "1111111111", "password": "12345"})
        mock_user_1 = json.dumps({"first_name": "Nancy", "last_name": "Drew", "role": "MASTER", "phone": "1111167111"})
        self.client.post('/user', data=mock_user, headers={"Content-Type": "application/json"})
        self.client.post('/user', data=mock_user_1, headers={"Content-Type": "application/json"})
        get_response = self.client.get('/user')
        lst_of_users = get_response.get_json()
        sorted(lst_of_users, key=lambda user: user["phone"])
        # print(get_response.get_json())
        self.assertEqual(200, get_response.status_code)
        self.assertEqual("Becky", lst_of_users[0]["first_name"])
        self.assertEqual("Bells", lst_of_users[0]["last_name"])
        self.assertEqual("1111111111", lst_of_users[0]["phone"])
        self.assertEqual("CLIENT", lst_of_users[0]["role"])
        self.assertEqual("Nancy", lst_of_users[1]["first_name"])
        self.assertEqual("Drew", lst_of_users[1]["last_name"])
        self.assertEqual("1111167111", lst_of_users[1]["phone"])
        self.assertEqual("MASTER", lst_of_users[1]["role"])

    def test_user_put_user(self):
        """
        Check whether info is updated on the existing user by user_id
        """
        mock_user = json.dumps(
            {"first_name": "Jill", "last_name": "Zapata", "phone": "2211111111", "password": "12345"})
        response = self.client.post('/user', data=mock_user, headers={"Content-Type": "application/json"})
        user_id = response.json["id"]
        info_to_update = json.dumps({"first_name": "Mill", "last_name": "Zapata", "role": "MASTER",
                                     "phone": "2211111111"})
        update_response = self.client.put(f'/user/{user_id}', data=info_to_update,
                                          headers={"Content-Type": "application/json"})
        self.assertEqual(200, update_response.status_code)
        self.assertEqual("Mill", update_response.json["first_name"])
        self.assertEqual("MASTER", update_response.json["role"])

    def test_user_get_by_id(self):
        """Tests whether get response gets existing user by_id"""
        mock_user_1 = json.dumps(
            {"first_name": "Curt", "last_name": "Weller", "phone": "3311111111", "password": "12345"})
        response_1 = self.client.post('/user', data=mock_user_1, headers={"Content-Type": "application/json"})
        user_id_1 = response_1.json["id"]
        get_response = self.client.get(f'/user/{user_id_1}')
        self.assertEqual(200, get_response.status_code)
        self.assertEqual("Curt", get_response.json["first_name"])
        self.assertEqual("Weller", get_response.json["last_name"])
        self.assertEqual("3311111111", get_response.json["phone"])
        self.assertEqual("CLIENT", get_response.json["role"])

    def test_user_delete(self):
        """
        Tests that user is deleted by user_id
        """
        mock_user = json.dumps(
            {"first_name": "Curt", "last_name": "Weller", "phone": "3311111111", "role": "MASTER", "password": "12345"})
        response = self.client.post('/user', data=mock_user, headers={"Content-Type": "application/json"})
        user_id = response.json["id"]
        delete_response = self.client.delete(f'/user/{user_id}')
        deleted_user_query = user.get_user(user_id)
        self.assertEqual(200, delete_response.status_code)
        self.assertEqual(None, deleted_user_query)

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
