from blackrock.blackrock_main.models import LastImportDate
from smoketest import SmokeTest


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = LastImportDate.objects.all().count()
        self.assertTrue(cnt > 0)
