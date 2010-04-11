from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User
from blackrock.respiration.models import Temperature
import datetime


class ModelTestCases(TestCase):

  def _a_little_test_data(self):
      Temperature.objects.get_or_create(station='Open Lowland', date=datetime.datetime(1997, 1, 1, 1, 00), reading=1.1)
      Temperature.objects.get_or_create(station='Open Lowland', date=datetime.datetime(2008, 6, 1, 1, 00), reading=1.1)
      Temperature.objects.get_or_create(station='Ridgetop', date=datetime.datetime(2008, 7, 1, 1, 00), reading=1.1)
      Temperature.objects.get_or_create(station='Fire Tower', date=datetime.datetime(2008, 8, 1, 1, 00), reading=1.1)
      
      self.assertEquals(Temperature.objects.filter(station='Open Lowland').count(), 2)
      self.assertEquals(Temperature.objects.filter(station='Ridgetop').count(), 1)
      self.assertEquals(Temperature.objects.filter(station='Fire Tower').count(), 1)
          
  def test_selective_delete(self):
      # All Data
      self._a_little_test_data()
      self.assertEquals(Temperature.selective_delete(None, None, None), 4)
      self.assertEquals(Temperature.objects.all().count(), 0)
      
      # One Station, no date range
      self._a_little_test_data()
      Temperature.selective_delete('Open Lowland', None, None)
      self.assertEquals(Temperature.objects.filter(station='Open Lowland').count(), 0)
      self.assertEquals(Temperature.objects.filter(station='Ridgetop').count(), 1)
      self.assertEquals(Temperature.objects.filter(station='Fire Tower').count(), 1)
      
      # One Station, date range
      self._a_little_test_data()
      Temperature.selective_delete('Open Lowland', datetime.datetime(2008, 1, 1), datetime.datetime(2008, 12, 31))
      qs = Temperature.objects.filter(station='Open Lowland')
      self.assertEquals(qs.count(), 1)
      self.assertEquals(qs[0].date, datetime.datetime(1997, 1, 1, 1, 00))
      self.assertEquals(Temperature.objects.filter(station='Ridgetop').count(), 1)
      self.assertEquals(Temperature.objects.filter(station='Fire Tower').count(), 1)
      
      
