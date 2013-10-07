#test_views.py


from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.contrib.auth.models import User


class TestPortalViews(TestCase):

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()


    #def test_index(self):
    #    response = self.c.get('/')
    #    self.assertEqual(response.status_code, 302)
    #    self.assertTemplateUsed('mammals/index.html')