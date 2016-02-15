from django.core.management.base import BaseCommand
from blackrock.waterquality.models import Site, Location, Series, Row
import csv
from datetime import datetime, timedelta

months = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8,
              Sep=9, Oct=10, Nov=11, Dec=12)


def fixdatetime(year, jul_day, hour):
    year = int(year)
    jul_day = int(jul_day)
    j1 = datetime(year=year, month=1, day=1)
    h = int(hour) / 100
    t = timedelta(days=jul_day, hours=h)
    d = j1 + t
    return "%d-%02d-%02d %02d:00:00" % (d.year, d.month, d.day, d.hour)


def prep_the_series(columns, units, names, location):
    series_objects = dict()
    for (column, unit, name) in zip(columns, units, names):
        (series, created) = Series.objects.get_or_create(
            name=name, location=location, units=unit)
        if not created:
            print "clearing out %s" % name
            series.row_set.all().delete()

        series_objects[column] = series
    return series_objects


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        print "importing BRF Lowlands data"
        (site, created) = Site.objects.get_or_create(name='BRF')
        (location, created) = Location.objects.get_or_create(
            name='Lowlands', site=site)

        reader = csv.reader(
            open("waterquality/xls/BRF_Open_Lowlands_2009.csv"))
        # all_columns = ["Array ID","Year","Jul_Day","Hour","TEMP_C_AVG",
        #                "TEMP_C_MAX","TEMP_C_MIN","RH___AVG",
        #                "RH___MAX","RH___MIN","VP_kPa_AVG",
        #                "DewPt_C_AVG","PAR_PPFD_TOT","GSR_W_m2_AVG",
        #                "Wspd_m_s_S_WVT","Wdir_deg_D1_WVT",
        #                "Wdir_deg_SD1_WVT","Wspd_m_s_MAX","Rain_mm_TOT",
        #                "BP_mbar_AVG","BP_mbar_MAX","Ref_temp",
        #                "BP_mbar_MIN","STEMP_10_AVG","STEMP_20_AVG",
        #                "BattVolt","CO2"]

        columns = [4, 18]
        names = ["BRF Lowlands Temp", "BRF Lowlands Rainfall"]
        units = ["Celsius", "mm"]

        series_objects = prep_the_series(columns, units, names, location)

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
