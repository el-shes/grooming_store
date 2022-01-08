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

    def test_validate_user(self):
        """
        Validates user's information passed on registration
        """
        mock_user = {"first_name": "Mary Jane", "last_name": "Bill's", "role": "CLIENT", "phone": "5555665577"}
        result = user.validate_on_create(mock_user)
        self.assertFalse(result)

    def test_validate_wrong_first_name_user(self):
        """
        Validates user with wrong first_name
        """
        mock_user = {"first_name": "M/ane", "last_name": "Bill's", "role": "MASTER", "phone": "1234567890"}
        result = user.validate_on_create(mock_user)
        self.assertTrue(result)
        self.assertTrue("first_name" in result)
        self.assertEqual(result["first_name"], "Invalid symbol")

    def test_validate_blank_first_user_input_user(self):
        """
        Validates user with blank first_name input
        """
        mock_user = {"first_name": "", "last_name": "Bill's", "role": "MASTER", "phone": "1234567890"}
        result = user.validate_on_create(mock_user)
        self.assertTrue(result)
        self.assertTrue("first_name" in result)
        self.assertEqual(result["first_name"], "Cannot be empty")

    def test_validate_wrong_last_name_user(self):
        """
        Validates user with wrong last_name
        """
        mock_user = {"first_name": "Jack", "last_name": "Bi#s", "role": "ADMIN", "phone": "1234567890"}
        result = user.validate_on_create(mock_user)
        self.assertTrue(result)
        self.assertTrue("last_name" in result)
        self.assertEqual(result["last_name"], "Invalid symbol")

    def test_validate_blank_last_name_input_user(self):
        """
        Validates user with blank last_name input
        """
        mock_user = {"first_name": "Jack", "last_name": "", "role": "ADMIN", "phone": "1234567890"}
        result = user.validate_on_create(mock_user)
        self.assertTrue(result)
        self.assertTrue("last_name" in result)
        self.assertEqual(result["last_name"], "Cannot be empty")

    def test_validate_wrong_role_user(self):
        """
        Validates wrong role for user
        """
        mock_user = {"first_name": "David", "last_name": "Schummer", "role": "USER", "phone": "1234567890"}
        result = user.validate_on_create(mock_user)
        self.assertTrue(result)
        self.assertTrue("role" in result)
        self.assertEqual(result["role"], "No such role")

    def test_validate_blank_role_input_user(self):
        """
        Validates user with blank role input
        """
        mock_user = {"first_name": "Davis", "last_name": "Mickels", "role": "", "phone": "1234567890"}
        result = user.validate_on_create(mock_user)
        self.assertTrue(result)
        self.assertTrue("role" in result)
        self.assertEqual(result["role"], "No such role")

    def test_validate_wrong_phone_user(self):
        """
        Validates wrong phone number input for user
        """
        mock_user = {"first_name": "Browny", "last_name": "Yum", "role": "CLIENT", "phone": "123456#890"}
        result = user.validate_on_create(mock_user)
        self.assertTrue(result)
        self.assertTrue("phone" in result)
        self.assertEqual(result["phone"], "Must contain numeric symbols and be of length 10")

    def test_validate_blank_phone_input_user(self):
        """
        Validates wrong phone number input for user
        """
        mock_user = {"first_name": "Bibi", "last_name": "Que", "role": "ADMIN", "phone": ""}
        result = user.validate_on_create(mock_user)
        self.assertTrue(result)
        self.assertTrue("phone" in result)
        self.assertEqual(result["phone"], "Must contain numeric symbols and be of length 10")

    def test_validate_phone_already_exists(self):
        """
        Validates phone number already exists in the database
        """
        user_1 = user.create_user("Nancy", "Joel", "123", "MASTER", "0123456789")
        mock_user = {"first_name": "Jei", "last_name": "Mark", "role": "MASTER", "phone": "0123456789"}
        result = user.validate_on_create(mock_user)
        self.assertTrue(result)
        self.assertTrue("phone" in result)
        self.assertEqual(result["phone"], "User with this phone number already exists")
        user.delete_user(user_1.id)
        db.session.commit()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
