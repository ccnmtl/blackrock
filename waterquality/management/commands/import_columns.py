from django.core.management.base import BaseCommand, CommandError
from data.models import Site,Location,Series,Row
import csv

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        columns = (('DO','mg/L'),('Temp','C'),('Depth','meters'),
                   ('ODOsat','%'),('Battery','volts'),('Sal','ppt'),
                   ('ODO2','mg/L'),('Sal2','ppt'))
        (site,created) = Site.objects.get_or_create(name='Harlem')
        (location,created) = Location.objects.get_or_create(name='H1',site=site)
        for column in columns:
            (series,created) = Series.objects.get_or_create(name=column[0],units=column[1],location=location)
            reader = csv.reader(open("columns/%s.csv" % column[0]))
            for row in reader:
                datetime = row[0]
                datum = row[1]
                r = Row.objects.create(series=series,
                                       timestamp=datetime,
                                       value=datum)

