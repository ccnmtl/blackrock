from blackrock.optimization.models import Plot, Tree
from django.test import TestCase
from django.contrib.gis.geos import Point


class TestOptimizationModels(TestCase):
    def setUp(self):
        self.plot_uni = Plot(name="new plot name",
                             area=12, width=4, height=3,
                             NW_corner=Point(12.4604, 43.9420))
        self.plot_uni.save()
        self.tree_uni = Tree(id=16, dbh=21, plot=self.plot_uni,
                             location=Point(12.4604, 43.9420))
        self.tree_uni.save()

    def test_uni(self):
        self.assertEquals(unicode(self.plot_uni),
                          self.plot_uni.name)
        self.assertEquals(unicode(self.tree_uni),
                          "Tree %d" % self.tree_uni.id)
