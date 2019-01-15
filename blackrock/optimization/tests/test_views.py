from django.test import TestCase, RequestFactory
from django.test.client import Client
from blackrock.optimization.views import (
    round2, comparison, format_time, variance)


class TestOptimizationViews(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_index(self):
        self.response = self.c.get('')
        self.assertEqual(self.response.status_code,  302)
        self.assertTemplateUsed('optimization/index.html')

    def test_run(self):
        self.response = self.c.get('/respiration/')
        self.assertEqual(self.response.status_code,  200)
        self.assertTemplateUsed('optimization/run.html')

    def test_calculate(self):
        pass

    def test_test(self):
        self.response = self.c.get('/test/')
        self.assertTemplateUsed('optimization/test.html')


class TestHelperFunctions(TestCase):
    def test_sample_plot(self):
        pass

    def test_json2csv(self):
        pass

    def test_trees_csv(self):
        pass

    def test_export_csv(self):
        pass

    def test_csv_details(self):
        pass

    def test_round2(self):
        self.assertEqual(99.35, round2(99.3455))

    def test_comparison(self):
        x = comparison(33.44, 55.33)
        self.assertEqual('60.44%', x)

    def test_format_time(self):
        self.assertEqual("1 hr, 39 min", format_time(99))
        self.assertEqual("2 hr", format_time(120))
        self.assertEqual("45 min", format_time(45))

    def test_variance(self):
        self.assertEqual(0, variance([1, 2, 3], 3, -2))
        self.assertEqual(1.0, variance([1, 2, 3], 3, 5))

    def test_load_csv(self):
        pass

    def test_tree_png(self):
        pass


class TestRandomSample(TestCase):
    pass
