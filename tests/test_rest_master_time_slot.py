import datetime
import json
import flask_restful
from flask import Flask
import unittest
from app import db
from rest import master_time_slots as time_slot_rest
from service import user as user_service, master, master_time_slot, procedure


class RestMasterTimeSlotTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)

        api = flask_restful.Api(self.app)
        api.add_resource(time_slot_rest.MasterTimeSlot, '/time-slot')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_post_master_time_slot(self):
        """
        Testing response on post operation while creating time_slot for master
        """
        user_master1 = user_service.create_user("Bibi", "Lime", "231", "MASTER", "3232523242")
        master1 = master.create_master(user_master1.id)
        user_id = user_master1.id
        master_id = master1.id
        mock_time_slot = json.dumps(
            {"date": "9/4/2022", "starting_hour": "10:00", "ending_hour": "15:00", "master_id": str(master1.id)})
        response = self.client.post('/time-slot', data=mock_time_slot, headers={"Content-Type": "application/json"})
        try:
            self.assertEqual(200, response.status_code)
            self.assertEqual('04-09-2022', response.json["date"])
            self.assertEqual('15:00:00', response.json["ending_hour"])
        finally:
            master_time_slot.delete_master_time_slot_by_id(response.json["id"])
            user_service.delete_user(user_id)
            master.delete_master(master_id)

    def test_get_master_time_slots(self):
        """
        Testing response on get time_slot operation
        """
        user_master1 = user_service.create_user("Chi", "Dale", "431", "MASTER", "3532523242")
        master1 = master.create_master(user_master1.id)
        user_id = user_master1.id
        master_id = master1.id
        procedure_id = procedure.create_procedure("Something", 200, 30).id
        date = datetime.datetime.strptime('9/4/2022', '%d/%m/%Y').date()
        starting = datetime.datetime.strptime('10:00', '%H:%M').time()
        ending = datetime.datetime.strptime('15:00', '%H:%M').time()
        created_slot = master_time_slot.create_master_time_slot(master_id,  date, starting, ending)
        slot_id = created_slot.id
        response = self.client.get(f'/time-slot?date=09-04-2022&master_id={master_id}&procedure_id={procedure_id}',
                                   headers={"Content-Type": "application/json"})
        try:
            print(response.get_json())
            self.assertEqual(200, response.status_code)
            self.assertEqual(20, len(response.json))
            self.assertEqual("10:00", response.json[0]["start"])
            self.assertEqual("10:30", response.json[0]["end"])
        finally:
            master_time_slot.delete_master_time_slot_by_id(slot_id)
            user_service.delete_user(user_id)
            master.delete_master(master_id)
            procedure.delete_procedure(procedure_id)

    def test_get_master_time_slots_2(self):
        """
        Testing response on get time_slot operation
        """
        user_master1 = user_service.create_user("Chi", "Dale", "431", "MASTER", "3532523242")
        master1 = master.create_master(user_master1.id)
        user_id = user_master1.id
        master_id = master1.id
        procedure_id = procedure.create_procedure("Something", 200, 30).id
        date = datetime.datetime.strptime('9/4/2022', '%d/%m/%Y').date()
        starting = datetime.datetime.strptime('10:00', '%H:%M').time()
        ending = datetime.datetime.strptime('14:00', '%H:%M').time()
        starting_2 = datetime.datetime.strptime('15:00', '%H:%M').time()
        ending_2 = datetime.datetime.strptime('19:00', '%H:%M').time()
        created_slot = master_time_slot.create_master_time_slot(master_id,  date, starting, ending)
        created_slot_2 = master_time_slot.create_master_time_slot(master_id,  date, starting_2, ending_2)
        slot_id = created_slot.id
        slot_id_2 = created_slot_2.id
        response = self.client.get(f'/time-slot?date=09-04-2022&master_id={master_id}&procedure_id={procedure_id}',
                                   headers={"Content-Type": "application/json"})
        try:
            print(response.get_json())
            self.assertEqual(200, response.status_code)
            self.assertEqual(26, len(response.json))
            self.assertEqual("10:00", response.json[0]["start"])
            self.assertEqual("10:30", response.json[0]["end"])
        finally:
            master_time_slot.delete_master_time_slot_by_id(slot_id)
            master_time_slot.delete_master_time_slot_by_id(slot_id_2)
            user_service.delete_user(user_id)
            master.delete_master(master_id)
            procedure.delete_procedure(procedure_id)

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()