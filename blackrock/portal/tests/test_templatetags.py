from django.test.testcases import TestCase

from blackrock.portal.templatetags.portal import display_name
from blackrock.portal.tests.factories import AudienceFactory, \
    PersonFactory, FacetFactory, RegionFactory
from blackrock.portal.models import FeaturedAsset


class TestPortalTags(TestCase):

    def test_display_name(self):
        audience = AudienceFactory()
        self.assertTrue(display_name(audience).startswith('audience'))

        audience_name = "Featured %s" + audience.name
        facet = FacetFactory(name=audience_name)
        self.assertEquals(display_name(facet), "Sample Facet Display")

        fa = FeaturedAsset(audience=audience, asset_region=RegionFactory())
        self.assertEquals(fa.audience, audience)
        self.assertEquals(display_name(fa), "Featured Asset")

        self.assertEquals(display_name(PersonFactory()),
                          "John Doe")
