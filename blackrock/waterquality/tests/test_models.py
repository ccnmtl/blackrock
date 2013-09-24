from django.test import TestCase
from blackrock.waterquality.models import Site, Location, Series, Row
from datetime import datetime


class SiteTest(TestCase):
    def test__unicode(self):
        s = Site.objects.create(name="test")
        self.assertEqual(str(s), "test")


class LocationTest(TestCase):
    def test_unicode(self):
        s = Site.objects.create(name="test")
        l = Location.objects.create(name="test", site=s)
        self.assertEqual(str(l), "test")


class SeriesTest(TestCase):
    def series_factory(self):
        site = Site.objects.create(name="test")
        l = Location.objects.create(name="test", site=site)
        return Series.objects.create(name="test", location=l)

    def test_unicode(self):
        s = self.series_factory()
        self.assertEqual(str(s), "test")

    def test_get_absolute_url(self):
        s = self.series_factory()
        self.assertEqual(s.get_absolute_url(), "/series/%d/" % s.id)

    def test_count_empty(self):
        s = self.series_factory()
        self.assertEqual(s.count(), 0)

    def test_count_populated(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        self.assertEqual(s.count(), 1)

    def test_start(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        self.assertEqual(s.start().value, 1.0)

    def test_end(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        self.assertEqual(s.end().value, 1.0)

    def test_max(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        self.assertEqual(s.max(), 1.0)

    def test_min(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        self.assertEqual(s.min(), 1.0)

    def test_mean(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        self.assertEqual(s.mean(), 1.0)

    def test_stddev(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        self.assertEqual(s.stddev(), 0.0)

    def test_uq(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=2.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=3.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=4.0)
        self.assertEqual(s.uq(), 3.0)

    def test_lq(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=2.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=3.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=4.0)
        self.assertEqual(s.lq(), 2.0)

    def test_median(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=2.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=3.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=4.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=5.0)
        self.assertEqual(s.median(), 3.0)

    def test_test_data(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        self.assertEqual(s.test_data(points=1)[0], 1.0)

    def test_box_data(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=2.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=3.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=4.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=5.0)
        r = s.box_data()
        self.assertEqual(r['min'], 0.0)
        self.assertEqual(r['max'], 100.0)
        self.assertEqual(r['lq'], 25.0)
        self.assertEqual(r['uq'], 75.0)
        self.assertEqual(r['median'], 50.0)

    def test_range_data(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=2.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=3.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=4.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=5.0)
        r = s.range_data()
        self.assertEqual(r, [1.0, 2.0, 3.0, 4.0, 5.0])

    def test_range_data_constrained(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        row1 = Row.objects.create(
            series=s, timestamp=datetime.now(), value=2.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=3.0)
        row2 = Row.objects.create(
            series=s, timestamp=datetime.now(), value=4.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=5.0)
        r = s.range_data(start=row1.timestamp, end=row2.timestamp)
        self.assertEqual(r, [2.0, 3.0, 4.0])

    def test_range_data_sampled(self):
        s = self.series_factory()
        Row.objects.create(series=s, timestamp=datetime.now(), value=1.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=2.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=3.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=4.0)
        Row.objects.create(series=s, timestamp=datetime.now(), value=5.0)
        # is this actually a fencepost error?
        r = s.range_data(max_points=2)
        self.assertEqual(r, [1.0, 3.0, 5.0])
