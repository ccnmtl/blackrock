from django.core.management.base import BaseCommand
from waterquality.models import Row,Series
from datetime import timedelta

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        series = Series.objects.get(id=args[0])
        start_date = series.row_set.all()[0].timestamp
        end_date = series.row_set.all().order_by("-timestamp")[0].timestamp
        step_date = start_date
        d = timedelta(hours=1)
        missing = 0
        found = 0
        while step_date < end_date:
            r = series.row_set.filter(timestamp=step_date)
            if r.count() == 0:
                missing += 1
                r = Row.objects.create(series=series,timestamp=step_date,value="0.0")
            else:
                found += 1
            step_date = step_date + d

        print "filled in %d" % missing
        print "total: %d" % series.row_set.all().count()
