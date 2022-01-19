import datetime
import json
import flask_restful
from flask import Flask
import unittest
from app import db
from rest import reservation as reservation_rest
from service import reservation, user, master, breed, procedure, jwt, master_time_slot


class RestReservationTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)

        api = flask_restful.Api(self.app)

        api.add_resource(reservation_rest.Reservation, '/reservation')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_post_reservation(self):
        """
        Testing post response on reservation creation
        """
        # master_id, client_id, breed_id, procedure_id, time_from, time_to, date
        user_client = user.create_user("Reo", "Bailey", "231", "CLIENT", "9032523242")
        user_master = user.create_user("Ethel", "Berry", "231", "MASTER", "8832523242")
        new_breed = breed.create_breed("Good boy", 2.2, 4.5, "image")
        new_procedure = procedure.create_procedure("Anything", 400, 60)
        master1 = master.create_master(user_master.id)
        user_client_id = user_client.id
        user_master_id = user_master.id
        user_role = user_client.role
        master_id = master1.id
        breed_id = new_breed.id
        procedure_id = new_procedure.id
        date = datetime.datetime.strptime('28/4/2022', '%d/%m/%Y').date()
        starting = datetime.datetime.strptime('9:00', '%H:%M').time()
        ending = datetime.datetime.strptime('15:00', '%H:%M').time()
        new_time_slot = master_time_slot.create_master_time_slot(master_id, date, starting, ending)
        new_time_slot_id = new_time_slot.id
        user_cookie = jwt.encode(user_client_id, user_role)
        mock_reservation = {"master_id": str(master_id), "breed_id": str(breed_id),
                            "procedure_id": str(procedure_id), "time_from": "10:00", "time_to": "11:00",
                            "date": '28/4/2022'}
        self.client.set_cookie('localhost', 'user', user_cookie)
        response = self.client.post('/reservation', data=mock_reservation)
        print(response.get_json())
        try:
            self.assertEqual(200, response.status_code)
        finally:
            procedure.delete_procedure(procedure_id)
            breed.delete_breed(breed_id)
            master.delete_master(master_id)
            user.delete_user(user_client_id)
            user.delete_user(user_master_id)
            master_time_slot.delete_master_time_slot_by_id(new_time_slot_id)
            reservation.delete_reservation(response.json["id"])

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
