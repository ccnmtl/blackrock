from django.core.management.base import BaseCommand, CommandError
from blackrock.portal.models import *

class Command(BaseCommand):
  
  def handle(self, *app_labels, **options):
      locations = Location.objects.all()
      
      for loc in locations:
          if loc.latlong == None:
              loc.latlong = "POINT(%s %s)" % (loc.latitude, loc.longitude)
              loc.save()
     