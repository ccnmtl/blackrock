from django.core.management.base import BaseCommand
import csv

months = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8,
              Sep=9, Oct=10, Nov=11, Dec=12)


def fixdatetime(date):
    print(date)
    (d, mon, y) = date.split("-")
    m = months[mon]
    return "%d-%02d-%02d" % (2000 + int(y), int(m), int(d))


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        reader = csv.reader(open("adf.csv"))
        all_columns = ["Station_ID", "Observation_Date", "High_Out__Temp_",
                       "Low_Out__Temp_", "Out_Tmp_High_Time",
                       "Out_Tmp_Low_Time", "High_Aux__Tmp", "Low_Aux__Tmp_",
                       "Aux_Tmp_High_Time", "Aux_Tmp__Low_Time", "Wind_Gust",
                       "Gust_Time", "Gust_Direction", "Max_Rain_Rate",
                       "Max_Rain_Rate_Time", "Monthly_Rainfall",
                       "Yearly_Rainfall", "High_Humidity", "Low_Humidity",
                       "High_Hum_Time", "Low_Hum_Time", "High_Pressure",
                       "Low_Pressure", "High_Press_Time", "Low_Press_Time",
                       "High_Light", "Low_Light", "High_Light_Time",
                       "Low_Light_Time", "Mx_Ltning_Rate_Rng1",
                       "Mx_Ltning_Rate_Rng2", "Mx_Ltning_Rate_Rng3",
                       "Indoor_Temp__High", "Indoor_Temp_Low",
                       "In_Tmp_High_Time", "In_Tmp__Low_Time"]
        date_col = 1

        columns = [2, 3, 6, 7, 10, 12, 13, 15, 16, 17, 18, 21, 22, 25, 26,
                   29, 30, 31, 32]
        writers = [csv.writer(open("columns/adf/%s.csv" % all_columns[c],
                                   "w")) for c in columns]
        for row in reader:
            datetime = fixdatetime(row[date_col])
            print(datetime)
            for ((idx), writer) in zip(columns, writers):
                columnname = all_columns[idx]
                print("-%s: %s" % (columnname, row[idx]))
                writer.writerow([datetime, row[idx]])
