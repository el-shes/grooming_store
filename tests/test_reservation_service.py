import datetime

from flask import Flask
import unittest
from app import db
from service import user, master, breed, procedure, reservation


class CreateUserTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def test_create_reservation(self):
        """
        Testing correct reservation creation
        """
        user_master = user.create_user("Ana", "Conda", "345", "MASTER", "1232124354")
        user_id = user.create_user("Betty", "Dove", "567", "CLIENT", "9878564313").id
        master_id = master.create_master(user_master.id).id
        breed_id = breed.create_breed("Big boy", 2.3, 1.5, "link").id
        procedure_id = procedure.create_procedure("Teeth whitening", 400, 30).id
        time_from = datetime.datetime.strptime('12:00', '%H:%M').time()
        time_to = datetime.datetime.strptime('13:00', '%H:%M').time()
        date = datetime.datetime.strptime('20/02/2022', '%d/%m/%Y').date()
        final_price = procedure.compute_total_procedure_price(procedure_id, breed_id)
        result = reservation.create_reservation(master_id, user_id, breed_id, procedure_id,
                                                time_from, time_to, date, final_price)
        self.assertTrue(result)
        self.assertEqual(master_id, result.master_id)
        self.assertEqual(user_id, result.client_id)
        self.assertEqual(breed_id, result.breed_id)
        self.assertEqual(procedure_id, result.procedure_id)
        self.assertEqual(1380, result.final_price)
        user.delete_user(user_master.id)
        user.delete_user(user_id)
        master.delete_master(master_id)
        breed.delete_breed(breed_id)
        procedure.delete_procedure(procedure_id)
        reservation.delete_reservation(result.id)
        db.session.commit()

    def test_delete_reservation(self):
        """
        Tests whether reservation is correctly deleted
        """
        user_master = user.create_user("Sindy", "Crow", "345", "MASTER", "3422124354")
        user_id = user.create_user("Lisel", "White", "567", "CLIENT", "9876664313").id
        master_id = master.create_master(user_master.id).id
        breed_id = breed.create_breed("Lil boy", 1.1, 1.2, "link").id
        procedure_id = procedure.create_procedure("Paw whitening", 300, 60).id
        time_from = datetime.datetime.strptime('11:00', '%H:%M').time()
        time_to = datetime.datetime.strptime('12:00', '%H:%M').time()
        date = datetime.datetime.strptime('21/02/2022', '%d/%m/%Y').date()
        final_price = procedure.compute_total_procedure_price(procedure_id, breed_id)
        result = reservation.create_reservation(master_id, user_id, breed_id, procedure_id,
                                                time_from, time_to, date, final_price)
        reservation.delete_reservation(result.id)
        deleted_reservation_query = reservation.get_reservation_by_id(result.id)
        self.assertTrue(result)
        self.assertEqual(None, deleted_reservation_query)
        user.delete_user(user_master.id)
        user.delete_user(user_id)
        master.delete_master(master_id)
        breed.delete_breed(breed_id)
        procedure.delete_procedure(procedure_id)
        reservation.delete_reservation(result.id)
        db.session.commit()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
