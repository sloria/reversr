'''Unit testing'''

from nose.tools import *
import app

import unittest
import tempfile

class ReversrTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        app.init_db()
        
