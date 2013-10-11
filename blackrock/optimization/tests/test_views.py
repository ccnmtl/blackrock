from blackrock.optimization.views import Species, index, run, calculate, RandomSample
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.contrib.auth.models import User
from blackrock.portal.models import Location

class TestOptimizationViews(TestCase):

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_run(self):
        self.response = self.c.get('/respiration/')
        self.assertEquals(self.response.status_code,  200)
        self.assertTemplateUsed('optimization/run.html')

    # def test_calculate(self):
    #     self.response = self.c.get('/sampler/calculate/')
    #     self.assertEquals(self.response.status_code,  200)


    # def test_trees(self):
    #     self.response = self.c.get('/trees.png/')
    #     self.assertEquals(self.response.status_code,  200)

    # def test_json2cvs(self):
    #     self.response = self.c.get('/csv/')
    #     self.assertEquals(self.response.status_code,  200)

    # def test_trees_csv(self):
    # 	self.response = self.c.get('/json2cvs/')
    #     self.assertEquals(self.response.status_code,  200)

    # def test_test(self):
    # 	self.response = self.c.get('/trees_csv/')
    #     self.assertEquals(self.response.status_code,  200)

    # def test_loadcsv(self):
    # 	self.response = self.c.get('/test/')
    #     self.assertEquals(self.response.status_code,  200)


