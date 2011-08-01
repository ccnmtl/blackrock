from django.core.management.base import BaseCommand
from waterquality.models import Site,Location,Series,Row
import csv

months = dict(Jan=1,Feb=2,Mar=3,Apr=4,May=5,Jun=6,Jul=7,Aug=8,Sep=9,Oct=10,
              Nov=11,Dec=12)

def fixdatetime(date):
    (d,m,y) = date.split("-")
    return "%d-%02d-%02d" % (2000 + int(y),int(months[m]),int(d))

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        print "importing Harlem River Rainfall data"
        (site,created) = Site.objects.get_or_create(name='Harlem')
        (location,created) = Location.objects.get_or_create(name='River',site=site)

        reader = csv.reader(open("waterquality/xls/HarlemRiver_rain_ambtemp.csv"))

        all_columns = ["Station_ID",       # 0
                       "Observation_Date", # 1
                       "High_Out__Temp_",  # 2
                       "Low_Out__Temp_",  # 3
                       "Out_Tmp_High_Time", # 4
                       "Out_Tmp_Low_Time", # 5
                       "High_Aux__Tmp", 
                       "Low_Aux__Tmp_",
                       "Aux_Tmp_High_Time",
                       "Aux_Tmp__Low_Time",
                       "Wind_Gust", # 10
                       "Gust_Time",
                       "Gust_Direction",
                       "Max_Rain_Rate",
                       "Max_Rain_Rate_Time",
                       "Monthly_Rainfall", #15
                       "Yearly_Rainfall",
                       "High_Humidity",
                       "Low_Humidity",
                       "High_Hum_Time",
                       "Low_Hum_Time", #20
                       "High_Pressure",
                       "Low_Pressure",
                       "High_Press_Time",
                       "Low_Press_Time",
                       "High_Light", #25
                       "Low_Light",
                       "High_Light_Time",
                       "Low_Light_Time",
                       "Mx_Ltning_Rate_Rng1",
                       "Mx_Ltning_Rate_Rng2", #30
                       "Mx_Ltning_Rate_Rng3",
                       "Indoor_Temp__High",
                       "Indoor_Temp_Low",
                       "In_Tmp_High_Time",
                       "In_Tmp__Low_Time"] #35

        columns = [16]
        units = "mm"

        (series,created) = Series.objects.get_or_create(name="Harlem Daily Rainfall",location=location,units=units)

        if not created:
            # it already exists, so let's clear out all the data in that column
            series.row_set.all().delete()

        previous_days_rainfall = 0.0
        for row in reader:
            date = fixdatetime(row[1])
            yearly_rainfall = row[16]
            if row[1].startswith('01-Jan'):
                # special case for year turnover
                previous_days_rainfall = 0.0

            daily_rainfall = float(yearly_rainfall) - previous_days_rainfall
            previous_days_rainfall = float(yearly_rainfall)
            print date,yearly_rainfall, daily_rainfall
            for hour in range(24):
                datetime = date + " %02d:00:00" % hour
                r = Row.objects.create(series=series,timestamp=datetime,value=str(daily_rainfall * 25.4))



