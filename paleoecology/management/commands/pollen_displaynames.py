from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from optparse import make_option
from blackrock.paleoecology.models import *
import csv
import unicodedata

class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        args = 'Usage: python manage.py pollen_displaynames'
        objs = PollenType.objects.all()
        for obj in objs:
          if not obj.display_name or len(obj.display_name) < 1:
            obj.display_name = obj.name
            if obj.name.find(' (') >= 0 and obj.name != 'Spore (trilete)':
              obj.name = obj.name.split(' (')[0]
          obj.name = obj.name.replace('.', '')
          obj.name = obj.name.replace('(', '')
          obj.name = obj.name.replace(')', '')
          obj.name = obj.name.replace('/', '_')
          obj.name = unicodedata.normalize('NFKD', obj.name).encode('ascii','ignore') # remove any special characters
          obj.save()

        # hard-coded updates
        pt = PollenType.objects.get(name='Asteraceae')
        pt.display_name = 'Asteraceae (Ragweed & herbs)';
        pt.save()
        
        pt = PollenType.objects.get(name='Castanea dentata')
        pt.display_name = 'Castanea dentata (American Chestnut)'
        pt.save()
        
        pt = PollenType.objects.get(name='Fagus grandifolia')
        pt.display_name = 'Fagus grandifolia (American Beech)'
        pt.save()
        
        pt = PollenType.objects.get(name='Tsuga canadensis')
        pt.display_name = 'Tsuga canadensis (Eastern Hemlock)'
        pt.save()
        
        pt = PollenType.objects.get(name='Pinus subg Strobus')
        pt.display_name = 'Pinus subg. Strobus (White Pine)'
        pt.save()        

        
        
        
         
  