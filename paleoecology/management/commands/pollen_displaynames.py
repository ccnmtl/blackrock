from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from optparse import make_option
from blackrock.paleoecology.models import *
import csv

class Command(BaseCommand):
            
    def handle(self, *app_labels, **options):
        args = 'Usage: python manage.py pollen_displaynames'
        exceptions = ['Spore (trilete)', 'Organic matter (percent dry mass)']
        
        objs = PollenType.objects.all()
        for obj in objs:
          obj.display_name=obj.name
          if obj.name.find(' (') >= 0 and obj.name not in exceptions:
            obj.name = obj.name.split(' (')[0]
          obj.save()