from django.core.management.base import BaseCommand, CommandError
from data.models import Site,Location,Series,Row
import csv

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):

        columns = ["High_Out__Temp_",
                   "Low_Out__Temp_",
                   "High_Aux__Tmp",
                   "Low_Aux__Tmp_",
                   "Wind_Gust",
                   "Gust_Direction",
                   "Max_Rain_Rate",
                   "Monthly_Rainfall",
                   "Yearly_Rainfall",
                   "High_Humidity",
                   "Low_Humidity",
                   "High_Pressure",
                   "Low_Pressure",
                   "High_Light",
                   "Low_Light",
                   "Mx_Ltning_Rate_Rng1",
                   "Mx_Ltning_Rate_Rng2",
                   "Mx_Ltning_Rate_Rng3",
                   "Indoor_Temp__High"]

        (site,created) = Site.objects.get_or_create(name='Blackrock')
        (location,created) = Location.objects.get_or_create(name='B1',site=site)
        for column in columns:
            (series,created) = Series.objects.get_or_create(name=column,location=location)
            reader = csv.reader(open("columns/adf/%s.csv" % column))
            if not created:
                continue
            for row in reader:
                datetime = row[0]
                datum = row[1]
                r = Row.objects.create(series=series,
                                       timestamp=datetime,
                                       value=datum)
