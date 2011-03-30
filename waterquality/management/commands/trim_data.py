from django.core.management.base import BaseCommand
from waterquality.models import Row

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        print "TRIMMING TO MAIN DATE RANGE"
        Row.objects.filter(timestamp__lt="2009-04-24 00:00:00").delete()
        Row.objects.filter(timestamp__gt="2009-09-06 00:00:00").delete()
