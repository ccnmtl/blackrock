from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from blackrock.blackrock_main.views import loadsolr_poll
from django.http import HttpResponse


class TestStaff(TestCase):
    def setUp(self):
        '''Set up user in staff group for test.'''
        self.factory = RequestFactory()
        self.user, created = User.objects.get_or_create(username="staff")
        self.user.set_password("staff")
        self.user.is_staff = True
        self.user.save()

    def test_loadsolrpoll(self):
        self.request = self.factory.get('/loadsolrpoll/')
        self.request.user = self.user
        self.response = loadsolr_poll(self.request)
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(self.user.is_staff)
        self.assertEqual(type(self.response), HttpResponse)
