from django.core.management.base import BaseCommand
from data.models import Row,Series,Location,Site
from datetime import timedelta

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        for series in Series.objects.all():
            print "series: %s" % series.name
            start = series.start()
            end = series.end()
            d = timedelta(hours=1)
            timestamp = start.timestamp
            while timestamp < end.timestamp:
                r = series.row_set.filter(timestamp=timestamp)
                if r.count() != 1:
                    print series.name, series.id, timestamp, r.count()
                    for rr in r:
                        print rr.id, rr.value
                timestamp = timestamp + d
                    
