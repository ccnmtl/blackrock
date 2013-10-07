#test_views.py


from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.contrib.auth.models import User


class TestPortalViews(TestCase):

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()


    def test_nearby(self):
        response = self.c.get('nearby/56.0/58.2')
        self.assertTemplateUsed('portal/nearby.html')
    #    response = self.c.get('/')
    #    self.assertEqual(response.status_code, 302)
    #    self.assertTemplateUsed('mammals/index.html')@rendered_with('portal/nearby.html')

