from django.core.management.base import BaseCommand, CommandError
import csv

def fixdatetime(date,time):
    (m,d,y) = date.split("/")
    return "%d-%02d-%02d %s" % (int(y),int(m),int(d),time)

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        reader = csv.reader(open("oxygen.csv"))
        columns = (('DO',3),('Temp',10),('Depth',11),('ODOsat',12),('Battery',14),('Sal',16),('ODO2',17),('Sal2',18))
        writers = [csv.writer(open("columns/%s.csv" % c[0],"w")) for c in columns]
        for row in reader:
            datetime = fixdatetime(row[0],row[1])
            print datetime
            for ((columnname,idx),writer) in zip(columns,writers):
                print "-%s: %s" % (columnname,row[idx])
                writer.writerow([datetime,row[idx]])

