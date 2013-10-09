from blackrock.optimization.views import Species, index, run, calculate, RandomSample
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.contrib.auth.models import User
from blackrock.portal.models import Location

class TestOptimizationViews(TestCase):

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()