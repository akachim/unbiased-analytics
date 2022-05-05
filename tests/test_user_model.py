import unittest
from server.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = "Akachi")
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='Akachi')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password="Akachi")
        self.assertTrue(u.verify_password('Akachi'))
        self.assertFalse(u.verify_password("Victor"))


    def test_passsword_salts_are_random(self):
        u = User(password='Akachi')
        u2 = User(password = 'Akachi')
        self.assertTrue(u.password_hash != u2.password_hash)
        