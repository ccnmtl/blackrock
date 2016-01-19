from django.core.management.base import BaseCommand
from blackrock.waterquality.models import Row, Series
from datetime import timedelta
from decimal import Decimal


def make_rows(series, step_date, end_date, d):
    missing = 0
    found = 0
    while step_date < end_date:
        r = series.row_set.filter(timestamp=step_date)
        if r.count() == 0:
            missing += 1
            r = Row.objects.create(series=series,
                                   timestamp=step_date, value="0.0")
        else:
            found += 1
        step_date = step_date + d
    return (missing, found)


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        series = Series.objects.get(id=args[0])
        start_date = series.row_set.all()[0].timestamp
        end_date = series.row_set.all().order_by("-timestamp")[0].timestamp
        step_date = start_date
        d = timedelta(hours=1)
        (missing, found) = make_rows(series, step_date, end_date, d)

        print "filled in %d" % missing
        print "total: %d" % series.row_set.all().count()

        print "checking for duplicates now..."
        step_date = start_date
        duplicates = 0
        zero = Decimal("0.0")
        while step_date < end_date:
            r = series.row_set.filter(timestamp=step_date)
            if r.count() > 1:
                duplicates += r.count()
                # need to pick which duplicate(s) to delete
                # basically,  if there's a non-zero,  we prefer that one
                # otherwise,  just delete everything but the first
                has_non_zero = False
                for row in r:
                    if row.value != zero:
                        has_non_zero = True
                if not has_non_zero:
                    print "all zeros. delete all but first"
                    for row in r[1:]:
                        row.delete()
                else:
                    # clear out any zero values
                    remaining = r.count()
                    for row in r:
                        if remaining > 1:
                            if row.value == zero:
                                row.delete()
                                remaining = remaining - 1
                    if remaining > 1:
                        # more than one non-zero
                        delete_everything_but_the_first(r)
            step_date = step_date + d
        print "duplicates found: %d" % duplicates


def delete_everything_but_the_first(r):
    for row in r[1:]:
        row.delete()
