from django.core.management.base import BaseCommand
from waterquality.models import Row,Site,Location

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        print "TRIMMING HARLEM DATA TO MAIN DATE RANGE"
        (site,created) = Site.objects.get_or_create(name='Harlem')
        (location,created) = Location.objects.get_or_create(name='River',site=site)
        for s in location.series_set.all():
            Row.objects.filter(series=s,timestamp__lt="2009-04-24 00:00:00").delete()
            Row.objects.filter(series=s,timestamp__gt="2009-09-06 00:00:00").delete()
