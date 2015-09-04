from django.test.testcases import TestCase

from blackrock.portal.templatetags.portal import display_name
from blackrock.portal.tests.factories import FeaturedAssetFactory, \
    AudienceFactory, PersonFactory, FacetFactory


class TestPortalViews(TestCase):

    def test_display_name(self):
        self.assertEquals(display_name(AudienceFactory()),
                          "Sample Audience")

        self.assertEquals(display_name(FeaturedAssetFactory()),
                          "Featured Asset")

        self.assertEquals(display_name(PersonFactory()),
                          "John Doe")

        self.assertEquals(display_name(FacetFactory()),
                          "John Doe")
