from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from blackrock.respiration.models import Temperature, StationMapping
import datetime
from io import open
import os.path
import json
from django.core.cache import cache


class ImportTestCases(TestCase):
    # fixtures = ["test_data.json"]

    def _login(self, uname, pwd):
        # Do a fake login via the handy client login fixture
        self.assertTrue(self.client.login(username=uname, password=pwd))

        response = self.client.get('/admin/')
        self.assertContains(response, 'Respiration', status_code=200)

    def setUp(self):
        user = User(username="testuser", is_superuser="t", is_staff="t")
        user.set_password("test")
        user.save()

    def tearDown(self):
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

        self._login('testuser', 'test')

        response = self.client.get('/admin/respiration/')
        self.assertContains(response,
                            'Import Respiration Data From CSV',
                            status_code=200)

        # test existing data
        qs = Temperature.objects.filter(station='Test Station')
        self.assertEqual(qs.count(), 0)

        # Submitting files is a special case. To POST a file,
        # you need only provide the file field name as a key, and a file handle
        # to the file you wish to upload as a value.
        # The Test Client will populate the two POST field
        # (i.e., field and field_file required by Django's FileField.
        test_data_file = os.path.join(
            os.path.dirname(__file__), "test_respiration.csv")
        with open(test_data_file, 'rt', encoding='utf-8') as f:
            response = self.client.post(
                '/respiration/loadcsv', {'delete': 'on', 'csvfile': f})
            f.close()

            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                Temperature.objects.filter(station='Test Station').count(), 48)
            self.assertEqual(
                Temperature.objects.filter(station='Another Station').count(),
                24)

            # spotcheck
            my_date = datetime.datetime(1996, 12, 31, 0, 0)
            qs = Temperature.objects.filter(
                station='Test Station',
                date__year=my_date.year,
                date__month=my_date.month,
                date__day=my_date.day,
                date__hour=my_date.hour,
                date__minute=my_date.minute)
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs[0].reading, -0.72)

            # new station with invalid temp, after valid temps, should
            # register as 0 not, the other station's old temp
            qs = Temperature.objects.filter(
                station='Another Station',
                date=make_aware(datetime.datetime(1997, 1, 1, 0, 0)))
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs[0].reading, 0)

            # Check duplicate handling
            qs = Temperature.objects.filter(
                station='Test Station',
                date=datetime.datetime(1997, 1, 1, 23, 0))
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs[0].reading, -0.16)

            qs = Temperature.objects.filter(
                station='Test Station',
                date=datetime.datetime(1997, 1, 1, 22, 0))
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs[0].reading, -8.0)

            # Substituting last valid temp when temp is invalid
            qs = Temperature.objects.filter(
                station='Test Station',
                date=datetime.datetime(1996, 12, 31, 23, 0))
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs[0].reading, -2.16)

            qs = Temperature.objects.filter(
                station='Test Station',
                date=datetime.datetime(1997, 1, 1, 0, 0))
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs[0].reading, -2.16)

            qs = Temperature.objects.filter(
                station='Test Station',
                date=datetime.datetime(1997, 1, 1, 0o1, 0))
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs[0].reading, -2.16)

            qs = Temperature.objects.filter(
                station='Test Station',
                date=datetime.datetime(1997, 1, 1, 0o2, 0))
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs[0].reading, -1.06)

    def test_solr_import_set(self):
        Temperature.objects.get_or_create(
            station='Ridgetop',
            date=datetime.datetime(1997, 1, 1, 1, 0), reading=1.1)
        Temperature.objects.get_or_create(
            station='Ridgetop',
            date=datetime.datetime(2009, 1, 1, 1, 0), reading=1.1)
        Temperature.objects.get_or_create(
            station='Ridgetop',
            date=datetime.datetime(2009, 7, 1, 1, 0), reading=1.1)
        Temperature.objects.get_or_create(
            station='Ridgetop',
            date=datetime.datetime(2009, 8, 1, 1, 0), reading=1.1)

        StationMapping.objects.get_or_create(
            station="Open Lowland", abbreviation="OL")
        StationMapping.objects.get_or_create(
            station="Ridgetop", abbreviation="RT")
        StationMapping.objects.get_or_create(
            station="Fire Tower", abbreviation="FT")

        self._login('testuser', 'test')

        response = self.client.get('/admin/respiration/')
        self.assertContains(
            response, 'Import Respiration Data from SOLR', status_code=200)

        data = {'import_classification': 'RT_2009',
                'application': 'respiration',
                'collection_id': 'environmental-monitoring',
                'limit_records': '5'}

        response = self.client.post('/respiration/loadsolr', data)

        new_json = json.loads(response.content)
        self.assertEqual(new_json['complete'], True)

        self.assertTrue('solr_complete' in cache)
