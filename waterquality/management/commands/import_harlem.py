from django.core.management.base import BaseCommand
from waterquality.models import Site,Location,Series,Row
import csv

months = dict(Jan=1,Feb=2,Mar=3,Apr=4,May=5,Jun=6,Jul=7,Aug=8,Sep=9,Oct=10,
              Nov=11,Dec=12)

def fixdatetime(date,time):
    (m,d,y) = date.split("/")
    return "%d-%02d-%02d %s" % (int(y),int(m),int(d),time)

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        print "importing Harlem River data"
        (site,created) = Site.objects.get_or_create(name='Harlem')
        (location,created) = Location.objects.get_or_create(name='River',site=site)

        reader = csv.reader(open("waterquality/xls/HarlemRiver2009.csv"))
        all_columns = ["Date","Time","","ODO","","","","","","",
                       "Temp","Depth","ODOsat","","Battery",
                       "","Sal","ODO","Sal","","","",""]

        all_units = ["m/d/y","hh:mm:ss","","mg/L","","","","","","",
                     "C","meters","%","","volts","","ppt","mg/L",
                     "ppt","","","",""]


        columns = [3,10]
        units = ["mg/L","Celcius"]

        # prep the series
        series_objects = dict()
        for (column,unit) in zip(columns,units):
            (series,created) = Series.objects.get_or_create(name=all_columns[column],location=location,units=unit)
            series_objects[column] = series
        
        for row in reader:
            datetime = fixdatetime(row[0],row[1])
            for c in columns:
                series = series_objects[c]
                datum = row[c]
                if datum:
                    try:
                        r = Row.objects.create(series=series,
                                               timestamp=datetime,
                                               value=datum)
                    except Exception, e:
                        print "error with %s" % datum
                        print str(e)
