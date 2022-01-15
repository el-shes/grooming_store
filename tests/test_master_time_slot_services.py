import datetime
from flask import Flask
import unittest
from app import db
from service import master_time_slot, user, master, reservation, breed, procedure


class CreateProcedureTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def test_create_master_time_slot(self):
        """
        Tests whether the time slot is created correctly
        """
        mock_user = user.create_user("Mary", "Branch", "123", "MASTER", "0123456789")
        master_id = master.create_master(mock_user.id).id
        date = datetime.datetime.strptime('24/02/2022', '%d/%m/%Y').date()
        starting = datetime.datetime.strptime('10:00', '%H:%M').time()
        ending = datetime.datetime.strptime('16:00', '%H:%M').time()
        result = master_time_slot.create_master_time_slot(master_id, date, starting, ending)
        self.assertTrue(result)
        self.assertEqual(10, result.starting_hour.hour)
        self.assertEqual(16, result.ending_hour.hour)
        self.assertEqual(24, result.date.day)
        self.assertEqual(2, result.date.month)
        self.assertEqual(2022, result.date.year)
        user.delete_user(mock_user.id)
        master.delete_master(master_id)
        master_time_slot.delete_master_time_slot_by_id(result.id)
        db.session.commit()

    def test_update_master_time_slot(self):
        """
        Tests whether time slot is correctly updated
        """
        mock_user = user.create_user("Henry", "Ford", "123", "MASTER", "5656567887")
        master_id = master.create_master(mock_user.id).id
        date = datetime.datetime.strptime('22/02/2022', '%d/%m/%Y').date()
        starting = datetime.datetime.strptime('18:00', '%H:%M').time()
        ending = datetime.datetime.strptime('22:00', '%H:%M').time()
        created_slot = master_time_slot.create_master_time_slot(master_id, date, starting, ending)
        new_date = datetime.datetime.strptime('21/03/2022', '%d/%m/%Y').date()
        new_starting = datetime.datetime.strptime('16:00', '%H:%M').time()
        new_ending = datetime.datetime.strptime('21:00', '%H:%M').time()
        result = master_time_slot.update_master_time_slot(created_slot.id, master_id, new_date, new_starting,
                                                          new_ending)
        self.assertTrue(result)
        self.assertEqual(16, result.starting)
        self.assertEqual(21, result.ending)
        user.delete_user(mock_user.id)
        master.delete_master(master_id)
        master_time_slot.delete_master_time_slot_by_id(created_slot.id)
        db.session.commit()

    def test_get_all_slots(self):
        """
        Testing get on all time slots
        """
        mock_user1 = user.create_user("Steven", "Huskel", "123", "MASTER", "9090909090")
        mock_user2 = user.create_user("Bob", "Davis", "123", "MASTER", "8080909090")
        master_id1 = master.create_master(mock_user1.id).id
        master_id2 = master.create_master(mock_user2.id).id
        date = datetime.datetime.strptime('20/02/2022', '%d/%m/%Y').date()
        starting = datetime.datetime.strptime('12:00', '%H:%M').time()
        ending = datetime.datetime.strptime('20:00', '%H:%M').time()
        created_slot1 = master_time_slot.create_master_time_slot(master_id1, date, starting, ending)
        created_slot2 = master_time_slot.create_master_time_slot(master_id2, date, starting, ending)
        result = master_time_slot.get_all_slots()
        self.assertTrue(result)
        self.assertEqual(created_slot1.id, result[0].id)
        self.assertEqual(created_slot2.id, result[1].id)
        self.assertEqual(12, result[0].starting_hour)
        user.delete_user(mock_user1.id)
        user.delete_user(mock_user2.id)
        master.delete_master(master_id1)
        master.delete_master(master_id2)
        master_time_slot.delete_master_time_slot_by_id(created_slot1.id)
        master_time_slot.delete_master_time_slot_by_id(created_slot2.id)
        db.session.commit()

    def test_delete_master_time_slot(self):
        """
        Tests whether time slot is deleted correctly
        """
        mock_user = user.create_user("Steven", "Huskel", "123", "MASTER", "9090909090")
        master_id = master.create_master(mock_user.id).id
        date = datetime.datetime.strptime('20/02/2022', '%d/%m/%Y').date()
        starting = datetime.datetime.strptime('12:00', '%H:%M').time()
        ending = datetime.datetime.strptime('20:00', '%H:%M').time()
        created_slot = master_time_slot.create_master_time_slot(master_id, date, starting, ending)
        master_time_slot.delete_master_time_slot_by_id(created_slot.id)
        deleted_slot_query = master_time_slot.get_slot_by_id(created_slot.id)
        self.assertEqual(None, deleted_slot_query)

    def test_calculate_available_slots(self):
        """
        Testing that all available slots for a date are computed
        """
        mock_user = user.create_user("Steven", "Huskel", "123", "MASTER", "9090909090")
        master_id = master.create_master(mock_user.id).id
        date = datetime.datetime.strptime('20/02/2022', '%d/%m/%Y').date()
        created_slot_1 = master_time_slot.create_master_time_slot(master_id, date,
                                                                  datetime.datetime.strptime('09:00', '%H:%M').time(),
                                                                  datetime.datetime.strptime('14:00', '%H:%M').time())
        created_slot_2 = master_time_slot.create_master_time_slot(master_id, date,
                                                                  datetime.datetime.strptime('15:00', '%H:%M').time(),
                                                                  datetime.datetime.strptime('19:00', '%H:%M').time())

        user_id = user.create_user("Betty", "Dove", "567", "CLIENT", "9878564313").id
        breed_id = breed.create_breed("Big boy", 2.3, 1.5, "link").id
        mock_procedure = procedure.create_procedure("Teeth whitening", 400, 60)
        procedure_id = mock_procedure.id
        final_price = procedure.compute_total_procedure_price(procedure_id, breed_id)

        reservation_1 = reservation.create_reservation(master_id, user_id, breed_id, procedure_id,
                                                       datetime.datetime.strptime('10:00', '%H:%M').time(),
                                                       datetime.datetime.strptime('11:00', '%H:%M').time(), date,
                                                       final_price)
        reservation_2 = reservation.create_reservation(master_id, user_id, breed_id, procedure_id,
                                                       datetime.datetime.strptime('12:00', '%H:%M').time(),
                                                       datetime.datetime.strptime('13:30', '%H:%M').time(), date,
                                                       final_price)
        reservation_3 = reservation.create_reservation(master_id, user_id, breed_id, procedure_id,
                                                       datetime.datetime.strptime('15:00', '%H:%M').time(),
                                                       datetime.datetime.strptime('17:00', '%H:%M').time(), date,
                                                       final_price)
        try:
            available_reservations = master_time_slot.calculate_available_slots([created_slot_1, created_slot_2],
                                                                                [reservation_1, reservation_2,
                                                                                 reservation_3],
                                                                                mock_procedure.duration)
            # 9:00-10:00
            # 11:00-12:00
            # 17:00-18:00
            # 17:30-18:30
            # 18:00-19:00
            self.assertEqual(5, len(available_reservations))
            self.assertEqual(9, available_reservations[0]["start"].hour)
            self.assertEqual(10, available_reservations[0]["end"].hour)
            self.assertEqual(11, available_reservations[1]["start"].hour)
            self.assertEqual(12, available_reservations[1]["end"].hour)
            self.assertEqual(17, available_reservations[2]["start"].hour)
            self.assertEqual(18, available_reservations[2]["end"].hour)
            self.assertEqual(17, available_reservations[3]["start"].hour)
            self.assertEqual(30, available_reservations[3]["start"].minute)
            self.assertEqual(18, available_reservations[3]["end"].hour)
            self.assertEqual(30, available_reservations[3]["end"].minute)
            self.assertEqual(18, available_reservations[4]["start"].hour)
            self.assertEqual(19, available_reservations[4]["end"].hour)
        finally:
            user.delete_user(mock_user.id)
            master.delete_master(master_id)
            master_time_slot.delete_master_time_slot_by_id(created_slot_1.id)
            master_time_slot.delete_master_time_slot_by_id(created_slot_2.id)
            user.delete_user(user_id)
            breed.delete_breed(breed_id)
            procedure.delete_procedure(procedure_id)
            reservation.delete_reservation(reservation_1.id)
            reservation.delete_reservation(reservation_2.id)
            reservation.delete_reservation(reservation_3.id)
            db.session.commit()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
