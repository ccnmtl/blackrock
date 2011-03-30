from django.core.management.base import BaseCommand, CommandError
from data.models import Site,Location,Series,Row
import csv

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        columns = ["MinBatt_Volt","Depth_m","Cond_uScm",
                   "Temp_C","DO_mV","DO_ppm","pH",
                   "Liters_s","Depth_Ft","Flow"]
        (site,created) = Site.objects.get_or_create(name='Blackrock')
        (location,created) = Location.objects.get_or_create(name='B2',site=site)
        for column in columns:
            (series,created) = Series.objects.get_or_create(name=column,location=location)
            if not created:
                continue
            reader = csv.reader(open("columns/str/%s.csv" % column))
            for row in reader:
                datetime = row[0]
                datum = row[1]
                if datum:
                    r = Row.objects.create(series=series,
                                           timestamp=datetime,
                                           value=datum)

