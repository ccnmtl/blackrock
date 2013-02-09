from django.test import TestCase
from django.contrib.auth.models import User
from blackrock.respiration.models import Temperature, StationMapping
import datetime
import os.path
from django.utils import simplejson
from django.core.cache import cache
from blackrock_main.models import LastImportDate


class ImportTestCases(TestCase):
    # fixtures = ["test_data.json"]

    def _login(self, client, uname, pwd):
            # Do a fake login via the handy client login fixture
        self.assert_(client.login(username=uname, password=pwd))

        response = client.get('/admin/respiration/')
        self.assertContains(response, 'Respiration', status_code=200)

    def setUp(self):
        user = User(username="testuser", is_superuser="t", is_staff="t")
        user.set_password("test")
        user.save()

    def tearDown(self):
        User.objects.get(username="testuser").delete()
        Temperature.objects.all().delete()

    def test_csv_import(self):
        Temperature.objects.get_or_create(
            station='Open Lowland',
            date=datetime.datetime(1997, 1, 1, 1, 00),
            reading=1.1)
        Temperature.objects.get_or_create(
            station='Open Lowland',
            date=datetime.datetime(2008, 6, 1, 1, 00),
            reading=1.1)
        Temperature.objects.get_or_create(
            station='Ridgetop',
            date=datetime.datetime(2008, 7, 1, 1, 00),
            reading=1.1)
        Temperature.objects.get_or_create(
            station='Fire Tower',
            date=datetime.datetime(2008, 8, 1, 1, 00),
            reading=1.1)

        self._login(self.client, 'testuser', 'test')

        response = self.client.get('/admin/respiration/')
        self.assertContains(response,
                            'Import Respiration Data From CSV',
                            status_code=200)

        # test existing data
        qs = Temperature.objects.filter(station='Test Station')
        self.assertEquals(qs.count(), 0)

        # Submitting files is a special case. To POST a file,
        # you need only provide the file field name as a key, and a file handle
        # to the file you wish to upload as a value.
        # The Test Client will populate the two POST field
        # (i.e., field and field_file required by Django's FileField.
        test_data_file = os.path.join(
            os.path.dirname(__file__), "test_respiration.csv")
        f = open(test_data_file)
        response = self.client.post(
            '/respiration/loadcsv', {'delete': 'on', 'csvfile': f})
        f.close()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(
            Temperature.objects.filter(station='Test Station').count(), 48)
        self.assertEquals(
            Temperature.objects.filter(station='Another Station').count(), 24)

        # spotcheck
        qs = Temperature.objects.filter(
            station='Test Station',
            date=datetime.datetime(1996, 12, 31, 00, 00))
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -0.72)

        # new station with invalid temp, after valid temps, should register as
        # 0 not, the other station's old temp
        qs = Temperature.objects.filter(
            station='Another Station',
            date=datetime.datetime(1997, 1, 1, 00, 00))
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, 0)

        # Check duplicate handling
        qs = Temperature.objects.filter(
            station='Test Station', date=datetime.datetime(1997, 1, 1, 23, 00))
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -0.16)

        qs = Temperature.objects.filter(
            station='Test Station', date=datetime.datetime(1997, 1, 1, 22, 00))
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -8.0)

        # Substituting last valid temp when temp is invalid
        qs = Temperature.objects.filter(
            station='Test Station',
            date=datetime.datetime(1996, 12, 31, 23, 00))
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -2.16)

        qs = Temperature.objects.filter(
            station='Test Station', date=datetime.datetime(1997, 1, 1, 00, 00))
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -2.16)

        qs = Temperature.objects.filter(
            station='Test Station', date=datetime.datetime(1997, 1, 1, 01, 00))
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -2.16)

        qs = Temperature.objects.filter(
            station='Test Station', date=datetime.datetime(1997, 1, 1, 02, 00))
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -1.06)

    def test_solr_import_set(self):
        Temperature.objects.get_or_create(
            station='Ridgetop',
            date=datetime.datetime(1997, 1, 1, 1, 00), reading=1.1)
        Temperature.objects.get_or_create(
            station='Ridgetop',
            date=datetime.datetime(2009, 1, 1, 1, 00), reading=1.1)
        Temperature.objects.get_or_create(
            station='Ridgetop',
            date=datetime.datetime(2009, 7, 1, 1, 00), reading=1.1)
        Temperature.objects.get_or_create(
            station='Ridgetop',
            date=datetime.datetime(2009, 8, 1, 1, 00), reading=1.1)

        StationMapping.objects.get_or_create(
            station="Open Lowland", abbreviation="OL")
        StationMapping.objects.get_or_create(
            station="Ridgetop", abbreviation="RT")
        StationMapping.objects.get_or_create(
            station="Fire Tower", abbreviation="FT")

        self._login(self.client, 'testuser', 'test')

        response = self.client.get('/admin/respiration/')
        self.assertContains(
            response, 'Import Respiration Data from SOLR', status_code=200)

        data = {'import_classification': 'RT_2009',
                'application': 'respiration',
                'collection_id': 'environmental-monitoring',
                'limit_records': '5'}

        response = self.client.post('/respiration/loadsolr', data)

        json = simplejson.loads(response.content)
        self.assertEquals(json['complete'], True)

        self.assertTrue('solr_complete' in cache)
        self.assertFalse('solr_error' in cache)
        self.assertEquals(cache.get('solr_created'), 4)
        self.assertEquals(cache.get('solr_updated'), 1)

        qs = Temperature.objects.filter(station='Ridgetop').order_by('date')
        self.assertEquals(qs.count(), 8)
        self.assertEquals(qs[0].date, datetime.datetime(1997, 1, 1, 1, 0))

        self.assertEquals(qs[1].date, datetime.datetime(2009, 1, 1, 0, 0))
        self.assertEquals(qs[1].reading, -13.01)

        self.assertEquals(qs[2].date, datetime.datetime(2009, 1, 1, 1, 0))
        self.assertEquals(qs[2].reading, -13.119999999999999)

        self.assertEquals(qs[3].date, datetime.datetime(2009, 1, 1, 2, 0))
        self.assertEquals(qs[3].reading, -13.34)

        response = self.client.get('/blackrock_main/loadsolrpoll', {})
        json = simplejson.loads(response.content)
        self.assertEquals(json['solr_created'], 4)
        self.assertEquals(json['solr_updated'], 1)

        self.assertFalse('solr_complete' in cache)
        self.assertFalse('solr_created' in cache)
        self.assertFalse('solr_updated' in cache)

        LastImportDate.objects.get(application='respiration')  # should exist
