from blackrock.portal.views import process_location, process_fieldnames
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.contrib.auth.models import User
from blackrock.portal.models import Location


class TestPortalViews(TestCase):

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_nearby(self):
        response = self.c.get('nearby/56.0/58.2')
        self.assertTemplateUsed('portal/nearby.html')

    def test_process_location(self):
    	pass_values = {"latitude" : "5", "longitude" : "9", "name" : "new test location"}
        self.test_process_location = process_location(pass_values)
        self.assertIsNotNone(self.test_process_location)
        #self.assertIsInstance(self.test_process_location, Location())

    def test_process_fieldnames(self):
        new_values = {"latitude" : "5", "longitude" : "9", "name" : "new test location"}
        self.process_fieldnames = process_fieldnames(new_values)
        self.assertIsNotNone(self.process_fieldnames)

    # def test_get_float(self):
    # 	self.float_test = get_float()


    # def test_process_metadata_exists(self):
    # 	# dataset object
    # 	self.metadata = {'dataset_id' : '111'}
    # 	self.metadata = {}


    # def test_process_metadata_does_not_exist(self):
    #     self.metadata = {'dataset_id' : '444'}

#    def test_process_fieldnames(self):
#    	pass_values = 


    #    response = self.c.get('/')
    #    self.assertEqual(response.status_code, 302)
    #    self.assertTemplateUsed('mammals/index.html')@rendered_with('portal/nearby.html')

    # def test_process_datasets()





