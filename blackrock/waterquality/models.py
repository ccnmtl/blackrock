from django.db import models
from django.utils import timezone


class Site(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=256)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=256)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    units = models.CharField(max_length=256, blank=True, default="")
    ordinality = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordinality']

    def get_absolute_url(self):
        return "/series/%d/" % self.id

    def __str__(self):
        return self.name

    def count(self):
        return self.row_set.all().count()

    def start(self):
        return Row.objects.filter(series=self).order_by("timestamp")[0]

    def end(self):
        return Row.objects.filter(series=self).order_by("-timestamp")[0]

    def max(self):
        return self.row_set.all().aggregate(max=models.Max('value'))['max']

    def min(self):
        return self.row_set.all().aggregate(min=models.Min('value'))['min']

    def mean(self):
        return self.row_set.all().aggregate(mean=models.Avg('value'))['mean']

    def stddev(self):
        return self.row_set.all().aggregate(
            stddev=models.StdDev('value'))['stddev']

    def uq(self):
        q = int(self.count() / 4)
        return self.row_set.all().order_by("-value")[q].value

    def lq(self):
        q = int(self.count() / 4)
        return self.row_set.all().order_by("value")[q].value

    def median(self):
        h = int(self.count() / 2)
        return self.row_set.all().order_by("value")[h].value

    def test_data(self, points=800):
        return [r.value for r in self.row_set.all()[:points]]

    def box_data(self):
        mn = self.min()
        max = self.max()
        chart_range = float(max) - float(mn)
        scale = 100.0 / chart_range
        return dict(min=float(mn - mn) * scale,
                    max=float(max - mn) * scale,
                    lq=float(self.lq() - mn) * scale,
                    uq=float(self.uq() - mn) * scale,
                    median=float(self.median() - mn) * scale)

    def range_data(self, start=None, end=None, max_points=800):
        if start is None:
            start = self.start().timestamp
        if end is None:
            end = self.end().timestamp
        rows = self.row_set.filter(timestamp__gte=start, timestamp__lte=end)
        inc = 1
        if rows.count() > max_points:
            # need to downsample so the graphing library can handle it
            inc = int(float(rows.count()) / max_points)
        return [r.value for r in rows[::inc]]


class LimitedSeries(object):
    """ a bundling of a Series with start/end range """
    def __init__(self, series, start=None, end=None, max_points=None):
        self.series = series
        if start is not None:
            self.start = start
        else:
            self.start = self.series.start().timestamp
        if end is not None:
            self.end = end
        else:
            self.end = self.series.end().timestamp

        if max_points is not None:
            self.max_points = max_points
        else:
            self.max_points = self.series.count()

    def row_set(self):
        return self.series.row_set.filter(
            timestamp__gte=self.start,
            timestamp__lte=self.end)

    def range_data(self, max_points=800):
        rows = self.row_set()
        inc = 1
        if rows.count() > max_points:
            # need to downsample so the graphing library can handle it
            inc = int(float(rows.count()) / max_points)
        return [r.value for r in rows[::inc]]

    def count(self):
        return self.row_set().count()

    def max(self):
        return self.row_set().aggregate(max=models.Max('value'))['max']

    def min(self):
        return self.row_set().aggregate(min=models.Min('value'))['min']

    def mean(self):
        return self.row_set().aggregate(mean=models.Avg('value'))['mean']

    def stddev(self):
        return self.row_set().aggregate(
            stddev=models.StdDev('value'))['stddev']

    def uq(self):
        q = int(self.count() / 4)
        return self.row_set().order_by("-value")[q].value

    def lq(self):
        q = int(self.count() / 4)
        return self.row_set().order_by("value")[q].value

    def median(self):
        h = int(self.count() / 2)
        return self.row_set().order_by("value")[h].value

    def sum(self):
        return self.row_set().aggregate(sum=models.Sum('value'))['sum']

    def box_data(self):
        mn = self.min()
        max = self.max()
        chart_range = float(max) - float(mn)
        scale = 100.0 / chart_range
        return dict(min=float(mn - mn) * scale,
                    max=float(max - mn) * scale,
                    lq=float(self.lq() - mn) * scale,
                    uq=float(self.uq() - mn) * scale,
                    median=float(self.median() - mn) * scale)


class LimitedSeriesGroup(object):
    def __init__(self, series):
        self.series = series

    def min(self):
        return min([s.min() for s in self.series])

    def max(self):
        return max([s.max() for s in self.series])

    def box_data(self):
        gmin = self.min()
        gmax = self.max()
        chart_range = float(gmax) - float(gmin)
        scale = 100.0 / chart_range
        data = []
        for s in self.series:
            data.append(dict(min=float(s.min() - gmin) * scale,
                             max=float(s.max() - gmin) * scale,
                             lq=float(s.lq() - gmin) * scale,
                             uq=float(s.uq() - gmin) * scale,
                             series=s,
                             median=float(s.median() - gmin) * scale))
        return dict(max=gmax, min=gmin, series=data,
                    count=len(data))


class LimitedSeriesPair(object):
    def __init__(self, independent, dependent, start=None,
                 end=None, skip_zeroes=None):
        self.independent = LimitedSeries(independent, start, end)
        self.dependent = LimitedSeries(dependent, start, end)
        self.skip_zeroes = skip_zeroes

    def linear_regression(self):
        count = self.independent.row_set().count()
        xs = [r.value for r in self.independent.row_set()]
        ys = [r.value for r in self.dependent.row_set()]
        sumx = self.independent.sum()
        sumy = self.dependent.sum()

        if self.skip_zeroes:
            # need to tweak things a bit
            newxs = []
            newys = []
            for x, y in zip(xs, ys):
                if x == 0 or y == 0 or x == 0.0 or y == 0.0:
                    continue
                newxs.append(x)
                newys.append(y)
            xs = newxs
            ys = newys
            count = len(xs)
            sumx = sum(xs)
            sumy = sum(ys)

        sumxx = sum([x * x for x in xs])
        sumxy = sum([x * y for x, y in zip(xs, ys)])
        det = (sumxx * count) - (sumx * sumx)
        if not det:
            # divide by zero
            return None
        a = (sumxy * count - sumy * sumx) / det
        b = (sumxx * sumy - sumx * sumxy) / det

        meanerror = sum([(y - sumy / count) ** 2 for y in ys])
        residual = sum([(y - a * x - b) ** 2 for x, y in zip(xs, ys)])

        if not meanerror:
            # divide by zero
            return None
        rr = 1.0 - (float(residual) / float(meanerror))

        ss = residual / (count - 2)

        var_a = ss * count / det
        var_b = ss * sumxx / det

        return dict(a=a, b=b, rr=rr, ss=ss, var_a=var_a, var_b=var_b)

    def regression_line_points(self):
        r = self.linear_regression()
        x1 = self.independent.min()
        x2 = self.independent.max()
        y1 = x1 * r['a'] + r['b']
        y2 = x2 * r['a'] + r['b']
        return [[x1, y1], [x2, y2]]


class Row(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.DecimalField(null=True, max_digits=19, decimal_places=10)

    class Meta:
        ordering = ['series', 'timestamp']
