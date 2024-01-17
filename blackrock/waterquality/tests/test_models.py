from __future__ import unicode_literals

from django.test import TestCase
from blackrock.waterquality.models import Site, Location, Series, Row
from blackrock.waterquality.models import LimitedSeries, LimitedSeriesGroup
from blackrock.waterquality.models import LimitedSeriesPair
from django.utils import timezone


class SiteTest(TestCase):
    def test_str(self):
        s = Site.objects.create(name="test")
        self.assertEqual(str(s), "test")


class LocationTest(TestCase):
    def test_str(self):
        s = Site.objects.create(name="test")
        loc = Location.objects.create(name="test", site=s)
        self.assertEqual(str(loc), "test")


def series_factory():
    site = Site.objects.create(name="test")
    loc = Location.objects.create(name="test", site=site)
    return Series.objects.create(name="test", location=loc)


class SeriesTest(TestCase):
    def test_unicode(self):
        s = series_factory()
        self.assertEqual(str(s), "test")

    def test_get_absolute_url(self):
        s = series_factory()
        self.assertEqual(s.get_absolute_url(), "/series/%d/" % s.id)

    def test_count_empty(self):
        s = series_factory()
        self.assertEqual(s.count(), 0)

    def test_count_populated(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        self.assertEqual(s.count(), 1)

    def test_start(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        self.assertEqual(s.start().value, 1.0)

    def test_end(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        self.assertEqual(s.end().value, 1.0)

    def test_max(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        self.assertEqual(s.max(), 1.0)

    def test_min(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        self.assertEqual(s.min(), 1.0)

    def test_mean(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        self.assertEqual(s.mean(), 1.0)

    def test_stddev(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        self.assertEqual(s.stddev(), 0.0)

    def test_uq(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        self.assertEqual(s.uq(), 3.0)

    def test_lq(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        self.assertEqual(s.lq(), 2.0)

    def test_median(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        self.assertEqual(s.median(), 3.0)

    def test_test_data(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        self.assertEqual(s.test_data(points=1)[0], 1.0)

    def test_box_data(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        r = s.box_data()
        self.assertEqual(r['min'], 0.0)
        self.assertEqual(r['max'], 100.0)
        self.assertEqual(r['lq'], 25.0)
        self.assertEqual(r['uq'], 75.0)
        self.assertEqual(r['median'], 50.0)

    def test_range_data(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        r = s.range_data()
        self.assertEqual(r, [1.0, 2.0, 3.0, 4.0, 5.0])

    def test_range_data_constrained(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        row1 = Row.objects.create(
            series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        row2 = Row.objects.create(
            series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        r = s.range_data(start=row1.timestamp, end=row2.timestamp)
        self.assertEqual(r, [2.0, 3.0, 4.0])

    def test_range_data_sampled(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        # is this actually a fencepost error?
        r = s.range_data(max_points=2)
        self.assertEqual(r, [1.0, 3.0, 5.0])


class LimitedSeriesTest(TestCase):
    def test_create_defaults(self):
        s = series_factory()
        rows = [
            Row.objects.create(series=s, timestamp=timezone.now(), value=1.0),
            Row.objects.create(series=s, timestamp=timezone.now(), value=2.0),
            Row.objects.create(series=s, timestamp=timezone.now(), value=3.0),
            Row.objects.create(series=s, timestamp=timezone.now(), value=4.0),
            Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)]
        ls = LimitedSeries(s)
        self.assertEqual(ls.max_points, 5)
        self.assertEqual(ls.start, rows[0].timestamp)
        self.assertEqual(ls.end, rows[-1].timestamp)

    def test_create(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=1, end=2, max_points=3)
        self.assertEqual(ls.max_points, 3)
        self.assertEqual(ls.start, 1)
        self.assertEqual(ls.end, 2)

    def test_row_set(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=r1.timestamp, end=r2.timestamp,
                           max_points=3)
        self.assertEqual(ls.row_set().count(), 3)

    def test_range_data(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=r1.timestamp, end=r2.timestamp,
                           max_points=3)
        self.assertEqual(ls.range_data(), [2.0, 3.0, 4.0])
        self.assertEqual(ls.range_data(max_points=1), [2.0])

    def test_count(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=r1.timestamp, end=r2.timestamp,
                           max_points=3)
        self.assertEqual(ls.count(), 3)

    def test_max(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=r1.timestamp, end=r2.timestamp,
                           max_points=3)
        self.assertEqual(ls.max(), 4.0)

    def test_min(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=r1.timestamp, end=r2.timestamp,
                           max_points=3)
        self.assertEqual(ls.min(), 2.0)

    def test_mean(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=r1.timestamp, end=r2.timestamp,
                           max_points=3)
        self.assertEqual(ls.mean(), 3.0)

    def test_stddev(self):
        s = series_factory()
        Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=r1.timestamp, end=r2.timestamp,
                           max_points=3)
        self.assertTrue(0.81 < ls.stddev() < 0.82)

    def test_uq(self):
        s = series_factory()
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=r1.timestamp, end=r2.timestamp,
                           max_points=3)
        self.assertEqual(ls.uq(), 4.0)

    def test_lq(self):
        s = series_factory()
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=r1.timestamp, end=r2.timestamp,
                           max_points=3)
        self.assertEqual(ls.lq(), 2.0)

    def test_median(self):
        s = series_factory()
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=r1.timestamp, end=r2.timestamp,
                           max_points=3)
        self.assertEqual(ls.median(), 3.0)

    def test_sum(self):
        s = series_factory()
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=r1.timestamp, end=r2.timestamp,
                           max_points=3)
        self.assertEqual(ls.sum(), 15.0)

    def test_box_data(self):
        s = series_factory()
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls = LimitedSeries(s, start=r1.timestamp, end=r2.timestamp,
                           max_points=3)
        r = ls.box_data()
        self.assertEqual(r['min'], 0.0)
        self.assertEqual(r['max'], 100.0)
        self.assertEqual(r['lq'], 25.0)
        self.assertEqual(r['uq'], 75.0)
        self.assertEqual(r['median'], 50.0)


class TestLimitedSeriesGroup(TestCase):
    def test_min(self):
        s = series_factory()
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        r3 = Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        r4 = Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls1 = LimitedSeries(s, start=r1.timestamp, end=r3.timestamp,
                            max_points=3)
        ls2 = LimitedSeries(s, start=r2.timestamp, end=r4.timestamp,
                            max_points=3)
        lsg = LimitedSeriesGroup([ls1, ls2])
        self.assertEqual(lsg.min(), 1.0)

    def test_max(self):
        s = series_factory()
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        r3 = Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        r4 = Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls1 = LimitedSeries(s, start=r1.timestamp, end=r3.timestamp,
                            max_points=3)
        ls2 = LimitedSeries(s, start=r2.timestamp, end=r4.timestamp,
                            max_points=3)
        lsg = LimitedSeriesGroup([ls1, ls2])
        self.assertEqual(lsg.max(), 5.0)

    def test_box_data(self):
        s = series_factory()
        r1 = Row.objects.create(series=s, timestamp=timezone.now(), value=1.0)
        r2 = Row.objects.create(series=s, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s, timestamp=timezone.now(), value=3.0)
        r3 = Row.objects.create(series=s, timestamp=timezone.now(), value=4.0)
        r4 = Row.objects.create(series=s, timestamp=timezone.now(), value=5.0)
        ls1 = LimitedSeries(s, start=r1.timestamp, end=r3.timestamp,
                            max_points=3)
        ls2 = LimitedSeries(s, start=r2.timestamp, end=r4.timestamp,
                            max_points=3)
        lsg = LimitedSeriesGroup([ls1, ls2])
        r = lsg.box_data()
        self.assertEqual(r['max'], 5.0)
        self.assertEqual(r['min'], 1.0)
        self.assertEqual(r['count'], 2)
        self.assertEqual(r['series'][0]['min'], 0.0)


class TestLimitedSeriesPair(TestCase):
    def test_linear_regression(self):
        s1 = series_factory()
        s2 = series_factory()

        Row.objects.create(series=s1, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=5.0)

        Row.objects.create(series=s2, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=5.0)

        lsp = LimitedSeriesPair(s1, s2)
        r = lsp.linear_regression()
        # dict(a=a, b=b, rr=rr, ss=ss, var_a=var_a, var_b=var_b)
        self.assertEqual(r['a'], 1.0)
        self.assertEqual(r['b'], 0.0)
        self.assertEqual(r['rr'], 1.0)
        self.assertEqual(r['ss'], 0.0)
        self.assertEqual(r['var_a'], 0.0)
        self.assertEqual(r['var_b'], 0.0)

    def test_linear_regression_skip_zeroes(self):
        s1 = series_factory()
        s2 = series_factory()

        Row.objects.create(series=s1, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=0.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=5.0)

        Row.objects.create(series=s2, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=5.0)

        lsp = LimitedSeriesPair(s1, s2, skip_zeroes=True)
        r = lsp.linear_regression()
        # dict(a=a, b=b, rr=rr, ss=ss, var_a=var_a, var_b=var_b)
        self.assertEqual(r['a'], 1.0)
        self.assertEqual(r['b'], 0.0)
        self.assertEqual(r['rr'], 1.0)
        self.assertEqual(r['ss'], 0.0)
        self.assertEqual(r['var_a'], 0.0)
        self.assertEqual(r['var_b'], 0.0)

    def test_linear_regression_divide_by_zero(self):
        s1 = series_factory()
        s2 = series_factory()

        Row.objects.create(series=s1, timestamp=timezone.now(), value=0.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=0.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=0.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=0.0)

        lsp = LimitedSeriesPair(s1, s2)
        r = lsp.linear_regression()
        self.assertEqual(r, None)

    def test_regression_line_points(self):
        s1 = series_factory()
        s2 = series_factory()

        Row.objects.create(series=s1, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s1, timestamp=timezone.now(), value=5.0)

        Row.objects.create(series=s2, timestamp=timezone.now(), value=1.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=2.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=3.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=4.0)
        Row.objects.create(series=s2, timestamp=timezone.now(), value=5.0)

        lsp = LimitedSeriesPair(s1, s2)
        r = lsp.regression_line_points()
        self.assertEqual(r, [[1.0, 1.0], [5.0, 5.0]])
