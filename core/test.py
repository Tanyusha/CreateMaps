from __future__ import unicode_literals, print_function, generators, division
from core import MDBDatabase
import os
import unittest
import pypyodbc

__author__ = 'pahaz'


class MdbTest(unittest.TestCase):

    def setUp(self):
        db_file = os.path.join(__file__, '..', '..', 'base.mdb')
        user = 'admin'
        password = 'Masterkey1'
        db = MDBDatabase(db_file, user, password)
        self.db = db

    def test_execute(self):
        db = self.db
        a, cols = db.execute('SELECT * FROM Users')
        self.assertIsInstance(a, list)

