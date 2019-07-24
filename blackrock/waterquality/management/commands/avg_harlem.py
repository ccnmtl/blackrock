from django.core.management.base import BaseCommand
from blackrock.waterquality.models import Row, Series, Location, Site
from datetime import timedelta


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        print("AVERAGING HARLEM DATA TO HOURLY")
        # use the BRF Stream as canonical for timestamps
        brf = Site.objects.get(name="BRF")
        stream = Location.objects.get(name="Stream", site=brf)
        # use any random series
        guide = stream.series_set.all()[0]

        # data to average
        harlem = Site.objects.get(name="Harlem")
        river = Location.objects.get(name="River", site=harlem)

        # a new location to put it in
        (averaged, created) = Location.objects.get_or_create(
            site=harlem, name="Averaged")

        for source in river.series_set.all():
            (dest_series, created) = Series.objects.get_or_create(
                location=averaged,
                name=source.name,
                units=source.units)
            previous_value = None
            for guide_row in guide.row_set.all():
                timestamp = guide_row.timestamp
                hourplus = timestamp + timedelta(hours=1)
                source_data = source.row_set.filter(timestamp__gte=timestamp,
                                                    timestamp__lt=hourplus)
                if source_data.count() > 0:
                    cnt = source_data.count()
                    total = sum([d.value for d in list(source_data)])
                    avg = total / cnt
                    Row.objects.create(
                        series=dest_series,
                        timestamp=timestamp,
                        value=avg)
                    previous_value = avg
                else:
                    # harlem is missing a bunch of data, so we'll just
                    # fill it in with the previous value
                    # best i can do for now

                    Row.objects.create(series=dest_series,
                                       timestamp=timestamp,
                                       value=previous_value)

        # rename shuffle
        river.delete()
        averaged.name = 'River'
        averaged.save()
