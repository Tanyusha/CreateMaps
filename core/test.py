from __future__ import unicode_literals, print_function, generators, division
from datetime import datetime
import tempfile
from core import MDBDatabase
from core.load_objects import load_objects, dump_objects
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


class SerializeTest(unittest.TestCase):
    def test_store_and_restore(self):
        DATA = [1, 2, 3]
        FILE_NAME = tempfile.mktemp()

        dump_objects(FILE_NAME, DATA)
        RESTORED = load_objects(FILE_NAME)
        self.assertEqual(DATA, RESTORED)

        os.remove(FILE_NAME)

    def test_object_with_datatime(self):
        DATA = [{'name': 'foo', 'type': 'bar', 'date': datetime.now()}]
        FILE_NAME = tempfile.mktemp()

        dump_objects(FILE_NAME, DATA)
        RESTORED = load_objects(FILE_NAME)
        self.assertEqual(DATA, RESTORED)

        os.remove(FILE_NAME)

    def test_object_with_empty_str(self):
        DATA = [{'name': '', 'type': '1'}]
        FILE_NAME = tempfile.mktemp()

        dump_objects(FILE_NAME, DATA)
        RESTORED = load_objects(FILE_NAME)
        self.assertEqual(DATA, RESTORED)

        os.remove(FILE_NAME)
