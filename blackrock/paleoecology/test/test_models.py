from blackrock.paleoecology.models import CoreSample, PollenType, PollenSample
from django.test import TestCase


class TestPortalModels(TestCase):
    def setUp(self):
        self.core_sample = CoreSample(depth=2.6)
        self.core_sample.save()
        self.pollen_type = PollenType(display_name="pollen display name")
        self.pollen_type.save()
        self.pollen_sample = PollenSample(
            core_sample=self.core_sample, pollen=self.pollen_type)
        self.pollen_sample.save()

    def test_the_unis(self):
        self.assertEqual(str(self.core_sample),
                         str(self.core_sample.depth))
        self.assertEqual(str(self.pollen_type),
                         self.pollen_type.display_name)
        self.assertEqual(str(self.pollen_sample),
                         '2.6 cm: 0 grains of  (0%)')
