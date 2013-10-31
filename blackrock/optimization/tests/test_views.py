from django.test import TestCase, RequestFactory
from django.test.client import Client


class TestOptimizationViews(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_run(self):
        self.response = self.c.get('/respiration/')
        self.assertEquals(self.response.status_code,  200)
        self.assertTemplateUsed('optimization/run.html')
