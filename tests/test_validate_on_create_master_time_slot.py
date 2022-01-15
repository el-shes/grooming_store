import datetime

from flask import Flask
import unittest
from app import db
from service import master_time_slot, user, master


class CreateProcedureTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def test_validate_correct_master_time_slot_creation(self):
        master_user = user.create_user("Test", "Tesst", "222", "MASTER", "7343526374")
        master_id = master.create_master(master_user.id).id
        time_from = datetime.datetime.strptime('10:00', '%H:%M').time()
        time_to = datetime.datetime.strptime('14:00', '%H:%M').time()
        date = datetime.datetime.strptime('11/04/2022', '%d/%m/%Y').date()
        result = master_time_slot.time_slot_validation(time_from, time_to, date, master_id)
        self.assertFalse(result)
        user.delete_user(master_user.id)
        master.delete_master(master_id)

    def test_validate_for_past_date(self):
        master_user = user.create_user("Test", "Tesstt", "422", "MASTER", "7342126374")
        master_id = master.create_master(master_user.id).id
        time_from = datetime.datetime.strptime('10:00', '%H:%M').time()
        time_to = datetime.datetime.strptime('14:00', '%H:%M').time()
        date = datetime.datetime.strptime('11/04/2021', '%d/%m/%Y').date()
        result = master_time_slot.time_slot_validation(time_from, time_to, date, master_id)
        self.assertTrue(result)
        self.assertTrue("date" in result)
        self.assertEqual("Can't put a time slot for past date", result["date"])
        user.delete_user(master_user.id)
        master.delete_master(master_id)

    def test_validate_time_slot_time_from_too_early(self):
        master_user = user.create_user("Keith", "Weitz", "442", "MASTER", "7342190374")
        master_id = master.create_master(master_user.id).id
        time_from = datetime.datetime.strptime('7:00', '%H:%M').time()
        time_to = datetime.datetime.strptime('14:00', '%H:%M').time()
        date = datetime.datetime.strptime('10/04/2022', '%d/%m/%Y').date()
        result = master_time_slot.time_slot_validation(time_from, time_to, date, master_id)
        self.assertTrue(result)
        self.assertTrue("time_from" in result)
        self.assertEqual("Slot should be placed from 9 to 20.30", result["time_from"])
        user.delete_user(master_user.id)
        master.delete_master(master_id)

    def test_validate_time_slot_time_from_too_late(self):
        master_user = user.create_user("John", "Nye", "482", "MASTER", "7662190374")
        master_id = master.create_master(master_user.id).id
        time_from = datetime.datetime.strptime('21:00', '%H:%M').time()
        time_to = datetime.datetime.strptime('21:00', '%H:%M').time()
        date = datetime.datetime.strptime('9/05/2022', '%d/%m/%Y').date()
        result = master_time_slot.time_slot_validation(time_from, time_to, date, master_id)
        self.assertTrue(result)
        self.assertTrue("time_from" in result)
        self.assertEqual("Slot should be placed from 9 to 20.30", result["time_from"])
        user.delete_user(master_user.id)
        master.delete_master(master_id)

    def test_time_slot_with_this_time_from_exists(self):
        master_user = user.create_user("Cassie", "Cline", "557", "MASTER", "5672198474")
        master_id = master.create_master(master_user.id).id
        created_time_from = datetime.datetime.strptime('9:00', '%H:%M').time()
        created_time_to = datetime.datetime.strptime('18:00', '%H:%M').time()
        date = datetime.datetime.strptime('9/05/2022', '%d/%m/%Y').date()
        time_slot = master_time_slot.create_master_time_slot(master_id, date, created_time_from, created_time_to)
        new_time_from = datetime.datetime.strptime('9:00', '%H:%M').time()
        new_time_to = datetime.datetime.strptime('15:00', '%H:%M').time()
        result = master_time_slot.time_slot_validation(new_time_from, new_time_to, date, master_id)
        self.assertTrue(result)
        self.assertTrue("time_from" in result)
        self.assertEqual("Slot with this starting time exists", result["time_from"])
        user.delete_user(master_user.id)
        master.delete_master(master_id)
        master_time_slot.delete_master_time_slot_by_id(time_slot.id)

    def test_validate_time_slot_time_to_too_early(self):
        master_user = user.create_user("Ilyas", "Denton", "552", "MASTER", "7662198474")
        master_id = master.create_master(master_user.id).id
        time_from = datetime.datetime.strptime('9:00', '%H:%M').time()
        time_to = datetime.datetime.strptime('9:00', '%H:%M').time()
        date = datetime.datetime.strptime('9/05/2022', '%d/%m/%Y').date()
        result = master_time_slot.time_slot_validation(time_from, time_to, date, master_id)
        self.assertTrue(result)
        self.assertTrue("time_to" in result)
        self.assertEqual("Slot should be placed from 9.30 to 21", result["time_to"])
        user.delete_user(master_user.id)
        master.delete_master(master_id)

    def test_validate_time_slot_time_to_too_late(self):
        master_user = user.create_user("Lily-May", "Connor", "552", "MASTER", "7662888474")
        master_id = master.create_master(master_user.id).id
        time_from = datetime.datetime.strptime('10:00', '%H:%M').time()
        time_to = datetime.datetime.strptime('22:00', '%H:%M').time()
        date = datetime.datetime.strptime('9/05/2022', '%d/%m/%Y').date()
        result = master_time_slot.time_slot_validation(time_from, time_to, date, master_id)
        self.assertTrue(result)
        self.assertTrue("time_to" in result)
        self.assertEqual("Slot should be placed from 9.30 to 21", result["time_to"])
        user.delete_user(master_user.id)
        master.delete_master(master_id)

    def test_time_slot_with_this_time_to_exists(self):
        master_user = user.create_user("Phoebe", "Armitage", "257", "MASTER", "5222198474")
        master_id = master.create_master(master_user.id).id
        created_time_from = datetime.datetime.strptime('14:00', '%H:%M').time()
        created_time_to = datetime.datetime.strptime('18:00', '%H:%M').time()
        date = datetime.datetime.strptime('9/05/2022', '%d/%m/%Y').date()
        time_slot = master_time_slot.create_master_time_slot(master_id, date, created_time_from, created_time_to)
        new_time_from = datetime.datetime.strptime('10:00', '%H:%M').time()
        new_time_to = datetime.datetime.strptime('18:00', '%H:%M').time()
        result = master_time_slot.time_slot_validation(new_time_from, new_time_to, date, master_id)
        print(result)
        self.assertTrue(result)
        self.assertTrue("time_to" in result)
        self.assertEqual("Slot with this ending time exists", result["time_to"])
        user.delete_user(master_user.id)
        master.delete_master(master_id)
        master_time_slot.delete_master_time_slot_by_id(time_slot.id)

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
