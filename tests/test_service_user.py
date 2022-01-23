from flask import Flask
import unittest
from app import db
from service import user


class CreateUserTest(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def test_create_user_service(self):
        """
        Testing correct user creation
        """
        mock_user = user.create_user("Emma-Louise", "Ryan", "123", "CLIENT", "1213234567")
        try:
            self.assertTrue(mock_user)
            self.assertEqual("Emma-Louise", mock_user.first_name)
            self.assertEqual("Ryan", mock_user.last_name)
            self.assertEqual("1213234567", mock_user.phone)
        finally:
            user.delete_user(mock_user.id)
            db.session.commit()

    def test_update_user(self):
        """
        Testing correct user update
        """
        mock_user = user.create_user("Naseem", "Miranda", "333", "CLIENT", "1342345675")
        info_to_update = {"first_name": "Laurel", "last_name": "Miranda", "role": "MASTER", "phone": "3342345675"}
        try:
            result = user.update_user(mock_user.id, info_to_update["first_name"], info_to_update["last_name"],
                                      info_to_update["role"], info_to_update["phone"])
            self.assertTrue(result)
            self.assertEqual("Laurel", result.first_name)
            self.assertEqual("Miranda", result.last_name)
            self.assertEqual("3342345675", result.phone)
        finally:
            user.delete_user(mock_user.id)
            db.session.commit()

    def test_get_by_id_correct_user(self):
        """
        Testing correct user get service by id
        """
        mock_user = user.create_user("Jane", "Eyer", "123", "CLIENT", "1231234567")
        found_user = user.get_user(mock_user.id)
        try:
            self.assertTrue(found_user)
            self.assertEqual("Jane", found_user.first_name)
            self.assertEqual("Eyer", found_user.last_name)
            self.assertEqual("1231234567", found_user.phone)
        finally:
            user.delete_user(found_user.id)
            db.session.commit()

    def test_delete_user(self):
        """
        Testing correct delete user service
        """
        mock_user = user.create_user("Arif", "Traynor", "1233", "ADMIN", "8831234567")
        user.delete_user(mock_user.id)
        found_user = user.get_user(mock_user.id)
        self.assertFalse(found_user)
        self.assertEqual(None, found_user)

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
