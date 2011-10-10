from django.core.management.base import BaseCommand
from waterquality.models import Site,Location,Series,Row
import csv

months = dict(Jan=1,Feb=2,Mar=3,Apr=4,May=5,Jun=6,Jul=7,Aug=8,Sep=9,Oct=10,
              Nov=11,Dec=12)

def fixdatetime(date,time):
    (m,d,y) = date.split("/")
    return "%d-%02d-%02d %s" % (int(y),int(m),int(d),time)

def get_datetime(row):
    date = row[0]
    hour = int(row[1].split(":")[0])
    return "%s %02d:00:00" % (date,hour)

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        print "importing HRECOS data"
        (site,created) = Site.objects.get_or_create(name='Harlem')
        (location,created) = Location.objects.get_or_create(name='HRECOS',site=site)

        reader = csv.reader(open("waterquality/xls/hrecos_data.csv"))
        all_columns = ["DATE (YYYY-MM-DD)",
                       "HOUR (1-24)",
                       "CONDUCTIVITY (ohms)",
                       "dO (ppm)",
                       "Temperature (Cels)"]

        all_units = ["YYYY-MM-DD","h:mm","ppm","mm","pH"]

        columns = [2,3,4]
        units = ["ohms","ppm","Celcius"]
        names = ["HRECOS Conductivity","HRECOS dO","HRECOS Temperature"]

        # prep the series
        series_objects = dict()
        for (column,unit,name) in zip(columns,units,names):
            (series,created) = Series.objects.get_or_create(name=name,location=location,units=unit)
            if not created:
                print "clearing out %s" % name
                series.row_set.all().delete()                

            series_objects[column] = series
        
        for row in reader:
            datetime = get_datetime(row)
            for c in columns:
                series = series_objects[c]
                datum = row[c] or "0.0"
                try:
                    r = Row.objects.create(series=series,
                                           timestamp=datetime,
                                           value=datum)
                except Exception, e:
                    print "error with %s" % datum
                    print str(e)
