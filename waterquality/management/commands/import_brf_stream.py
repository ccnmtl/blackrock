from django.core.management.base import BaseCommand
from waterquality.models import Site, Location, Series, Row
import csv
from datetime import datetime,  timedelta

months = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7,
              Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)


def fixdatetime(year, jul_day, hour):
    year = int(year)
    jul_day = int(jul_day)
    j1 = datetime(year=year, month=1, day=1)
    h = int(hour) / 100
    t = timedelta(days=jul_day, hours=h)
    d = j1 + t
    return "%d-%02d-%02d %02d:00:00" % (d.year, d.month, d.day, d.hour)


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self,  *args,  **options):
        print "importing BRF Stream data"
        (site, created) = Site.objects.get_or_create(name='BRF')
        (location,  created) = Location.objects.get_or_create(
            name='Stream', site=site)

        reader = csv.reader(open("waterquality/xls/BRF_Stream_2009.csv"))
        # all_columns = ["Array ID", "Year", "Jul_Day", "Hour",
        #                "MinBatt_Volt", "Depth _m", "Cond_uScm",
        #                "Temp_C", "DO_mV", "DO_ppm", "pH",
        #                "Liters_s", "Depth_Ft", "Flow Ft^3/s"]

        columns = [6, 7, 9, 10]
        names = ["Blackrock Forest Stream Conductivity", "Cascade Brook Temp",
                 "Cascade Brook DO", "Cascade Brook pH"]
        units = ["ohms", "Celsius", "mg/L", "ph"]

        # prep the series
        series_objects = dict()
        for (column, unit, name) in zip(columns, units, names):
            (series,  created) = Series.objects.get_or_create(
                name=name, location=location, units=unit)
            if not created:
                print "clearing out %s" % name
                series.row_set.all().delete()
            series_objects[column] = series

        for row in reader:
            datetime = fixdatetime(row[1], row[2], row[3])
            for c in columns:
                # BRF data has daily avgs mixed in. skip those.
                if row[0] == '24':
                    continue
                series = series_objects[c]
                datum = row[c]
                if datum:
                    try:
                        Row.objects.create(series=series,
                                           timestamp=datetime,
                                           value=datum)
                    except Exception, e:
                        print "error with %s" % datum
                        print str(e)
