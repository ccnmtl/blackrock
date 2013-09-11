from django.core.management.base import BaseCommand
import csv
from datetime import datetime, timedelta

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

    def handle(self, *args, **options):
        reader = csv.reader(open("str.csv"))
        all_columns = ["Array ID", "Year", "Jul_Day", "Hour",
                       "MinBatt_Volt", "Depth_m", "Cond_uScm",
                       "Temp_C", "DO_mV", "DO_ppm", "pH",
                       "Liters_s", "Depth_Ft", "Flow"]

        columns = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        writers = [csv.writer(open("columns/str/%s.csv" % all_columns[c],
                                   "w")) for c in columns]
        for row in reader:
            datetime = fixdatetime(row[1], row[2], row[3])
            print datetime
            for ((idx), writer) in zip(columns, writers):
                columnname = all_columns[idx]
                print "-%s: %s" % (columnname, row[idx])
                writer.writerow([datetime, row[idx]])
