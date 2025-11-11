import unittest

from pyramid import testing
from pyramid.response import Response

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from .tutorial.views import home

        request = testing.DummyRequest()
        response = home(request)
        self.assertEqual(response, 'Welcome!')

    def test_hello(self):
        from .tutorial.views import hello

        request = testing.DummyRequest()
        response = hello(request)
        self.assertEqual(response, 'Hello!')


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial import main
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'Welcome!', res.body)

    def test_hello(self):
        res = self.testapp.get('/howdy', status=200)
        self.assertIn(b'Hello!', res.body)
