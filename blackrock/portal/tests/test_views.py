from blackrock.portal.views import process_location, process_fieldnames
from django.test import TestCase, RequestFactory
from django.test.client import Client


class TestPortalViews(TestCase):

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_nearby(self):
        self.c.get('nearby/56.0/58.2')
        self.assertTemplateUsed('portal/nearby.html')

    def test_process_location(self):
        pass_values = {"latitude": "5", "longitude": "9",
                       "name": "new test location"}
        self.test_process_location = process_location(pass_values)
        self.assertIsNotNone(self.test_process_location)

    def test_process_fieldnames(self):
        new_values = {"latitude": "5", "longitude": "9",
                      "name": "new test location"}
        self.process_fieldnames = process_fieldnames(new_values)
        self.assertIsNotNone(self.process_fieldnames)
