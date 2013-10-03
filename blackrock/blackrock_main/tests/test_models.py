from django.test import TestCase
from blackrock.blackrock_main.models import LastImportDate


class LastImportDateTest(TestCase):
    def test_update_last_import_date(self):
        d = LastImportDate.update_last_import_date("foo")
        self.assertTrue(hasattr(d, 'year'))
        d2 = LastImportDate.update_last_import_date("foo")
        self.assertNotEqual(d, d2)

    def test_get_last_import_date(self):
        d = LastImportDate.get_last_import_date("2010-01-01", "13:15:00",
                                                "foo")
        self.assertTrue(d is not None)

    def test_get_last_import_date_invalid(self):
        d = LastImportDate.get_last_import_date("garbage", "more garbage",
                                                "foo")
        self.assertTrue(d is None)
