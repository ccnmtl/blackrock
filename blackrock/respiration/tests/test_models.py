from __future__ import unicode_literals

from django.test import TestCase
from django.utils.encoding import smart_text
from django.utils.timezone import make_aware
from blackrock.respiration.models import Temperature, StationMapping
import datetime


class ModelTestCases(TestCase):

    def _a_little_test_data(self):
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

        self.assertEqual(
            Temperature.objects.filter(station='Open Lowland').count(), 2)
        self.assertEqual(
            Temperature.objects.filter(station='Ridgetop').count(), 1)
        self.assertEqual(
            Temperature.objects.filter(station='Fire Tower').count(), 1)

    def test_selective_delete(self):
        # All Data
        self._a_little_test_data()
        self.assertEqual(Temperature.selective_delete(None, None, None), 4)
        self.assertEqual(Temperature.objects.all().count(), 0)

        # One Station, no date range
        self._a_little_test_data()
        Temperature.selective_delete('Open Lowland', None, None)
        self.assertEqual(
            Temperature.objects.filter(station='Open Lowland').count(), 0)
        self.assertEqual(
            Temperature.objects.filter(station='Ridgetop').count(), 1)
        self.assertEqual(
            Temperature.objects.filter(station='Fire Tower').count(), 1)

        # One Station, date range
        self._a_little_test_data()
        Temperature.selective_delete('Open Lowland', datetime.datetime(
            2008, 1, 1), datetime.datetime(2008, 12, 31))
        qs = Temperature.objects.filter(station='Open Lowland')
        self.assertEqual(qs.count(), 1)
        self.assertEqual(
            qs[0].date,
            make_aware(datetime.datetime(1997, 1, 1, 1, 00)))
        self.assertEqual(
            Temperature.objects.filter(station='Ridgetop').count(), 1)
        self.assertEqual(
            Temperature.objects.filter(station='Fire Tower').count(), 1)

    def test_station_mapping(self):
        self.station_mapping = StationMapping(station="new station",
                                              abbreviation="ns")
        self.assertEqual(
            str(self.station_mapping),
            "%s (%s)" % (self.station_mapping.station,
                         self.station_mapping.abbreviation))

    def test_temperature(self):
        self.temperature = Temperature(
            station='Open Lowland',
            date=datetime.datetime(1997, 1, 1, 1, 00))
        self.assertEqual(
            str(self.temperature),
            "%s: [No reading] at %s station" % (
                self.temperature.date, self.temperature.station))

    def test_temperature_two(self):
        self.temperature_2 = Temperature(
            station='Open Lowland',
            date=datetime.datetime(1997, 1, 1, 1, 00), reading=1.1)
        self.assertEqual(
            smart_text(self.temperature_2),
            "%s: %.2f\xb0 C at %s station" % (
                self.temperature_2.date,
                self.temperature_2.reading,
                self.temperature_2.station))
