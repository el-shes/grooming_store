import flask_restful
from flask import Flask
import unittest
from app import db
from rest import master_procedure as master_procedure_rest
from service import user, master, procedure, master_procedure


class RestMasterProcedureTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)

        api = flask_restful.Api(self.app)
        api.add_resource(master_procedure_rest.MasterProcedureById, '/master/procedure/<int:procedure_id>')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_master_procedure_get_masters(self):
        """
        Testing that get operation returns all masters by procedure id
        """
        user_master1 = user.create_user("Jessie", "Pine", "231", "MASTER", "3242523242")
        user_master2 = user.create_user("Alba", "Pine", "211", "MASTER", "2342523242")
        master1 = master.create_master(user_master1.id)
        master2 = master.create_master(user_master2.id)
        mock_procedure_id = procedure.create_procedure("Nothing", 300, 60).id
        master_procedure.add_mapping(master1.id, mock_procedure_id)
        master_procedure.add_mapping(master2.id, mock_procedure_id)
        try:
            get_response = self.client.get(f'/master/procedure/{mock_procedure_id}')
            lst_of_masters = get_response.get_json()
            existing_master1 = {}
            existing_master2 = {}
            for mstr in lst_of_masters:
                if mstr["id"] == master1.id:
                    existing_master1 = mstr
                elif mstr["id"] == master2.id:
                    existing_master2 = mstr
            print(get_response.get_json())
            self.assertEqual(200, get_response.status_code)
            self.assertEqual(master1.id, existing_master1["id"])
            self.assertEqual("Jessie Pine", existing_master1["name"])
            self.assertEqual(master2.id, existing_master2["id"])
            self.assertEqual("Alba Pine", existing_master2["name"])
        finally:
            user.delete_user(user_master1.id)
            user.delete_user(user_master2.id)
            master_procedure.del_mapping(master1.id, mock_procedure_id)
            master_procedure.del_mapping(master2.id, mock_procedure_id)
            master.delete_master(master1.id)
            master.delete_master(master2.id)
            procedure.delete_procedure(mock_procedure_id)

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
