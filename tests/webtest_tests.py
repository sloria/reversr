from unittest import TestCase
from webtest import TestApp
from nose.tools import *

from app import app

class TestAUser(TestCase):
    def setUp(self):
        self.app = TestApp(app)

    def tearDown(self):
        pass

    def test_can_see_homepage(self):
        # Goes to homepage
        res = self.app.get('/')
        assert_in('Upload an audio file', res)
        assert_equal(res.status_code, 200)

    def test_can_upload(self):
        assert False, 'finish me'