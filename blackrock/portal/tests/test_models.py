from blackrock.portal.models import Audience, DigitalFormat, Facet, Institution, LocationSubtype, LocationType, PersonType, PublicationType, RegionType, Tag, Url, DigitalObject, Location, Station
from django.test import TestCase
from datetime import datetime
#from django.contrib.auth.models import User
#from django.contrib.gis.db import models
#from django.utils import simplejson



class TestPortalModels(TestCase):

    def setUp(self):
        self.audience = Audience(name="audience name")
        self.audience.save()
        self.digital_format_image = DigitalFormat(name="png", id=1866)
        self.digital_format_image.save()
        self.digital_format_video = DigitalFormat(name="mp4", id=1200)
        self.digital_format_video.save()
        self.facet = Facet(name="facet name here", display_name="facet display name", facet="facet here...")
        self.facet.save()
        self.institution = Institution(name="institution name here")
        self.institution.save()
        self.location_subtype = LocationSubtype(name="location subtype name")
        self.location_subtype.save()
        self.location_type = LocationType(name="location type name")
        self.location_type.save()
        self.person_type = PersonType(name="special type of person")
        self.person_type.save()
        self.publication_type = PublicationType(name="publication name")
        self.publication_type.save()
        self.region_type = RegionType(name="region name")
        self.region_type.save()
        self.tag = Tag(name="tag name")
        self.tag.save()
        self.url = Url(name="http://www.ccnmtl.columbia.edu", display_name="ccnmtl.columbia.edu")
        self.url.save()
        self.digital_object = DigitalObject(name="digital object name", digital_format=self.digital_format_image)
        self.digital_object.save()
        self.location = Location(name="location name here",latitude=6.08,longitude=2.2)
        self.location.save()
        self.station = Station(name="station name", description="this is a station object", access_means="you can walk there!", activation_date=datetime.now(), location=self.location) # , audience=self.audience() has null=True in model - may be cause of problem, display_image=self.digital_object(), created_date=datetime.now(), modified_date=datetime.now() digital_object=self.digital_object, , tag=self.tag , 
        self.station.save()

    def test_audience_unicode(self):
        self.assertEquals(unicode(self.audience), self.audience.name)

    def test_digital_format_unicode(self):
        self.assertEquals(unicode(self.digital_format_image), self.digital_format_image.name)

    def test_digital_format_is_image(self):
        self.assertTrue(self.digital_format_image.is_image())

    def test_digital_format_is_video(self):
        self.assertTrue(self.digital_format_video.is_video())

    def test_facet_unicode(self):
        self.assertEquals(unicode(self.facet), self.facet.display_name)

    def test_facet_solr_name(self):
        self.assertEquals(self.facet.solr_name(), 'facet_here...')

    def test_institution_name(self):
        self.assertEquals(unicode(self.institution), "institution name here")#self.institution.name)

    def test_location_subtype(self):
        self.assertEquals(unicode(self.location_subtype), self.location_subtype.name)

    def test_location_type(self):
        self.assertEquals(unicode(self.location_type), self.location_type.name)

    def test_person_type(self):
        self.assertEquals(unicode(self.person_type), self.person_type.name)

    def test_publication_type(self):
        self.assertEquals(unicode(self.publication_type), self.publication_type.name)

    def test_region_type_uni(self):
        self.assertEquals(unicode(self.region_type), self.region_type.name)

    def test_tag_uni(self):
        self.assertEquals(unicode(self.tag), self.tag.name)

    def test_url_uni(self):
        self.assertEquals(unicode(self.url), self.url.name)

    def test_url_doc(self):
        self.assertEquals(self.url.document(), 'www.ccnmtl.columbia.edu')

    def test_digital_obj_uni(self):
        self.assertEquals(unicode(self.digital_object), self.digital_object.name)

    def test_location_uni(self):
       	self.assertEquals(unicode(self.location), "%s (%.6f,%.6f)" % (self.location.name, self.location.latitude, self.location.longitude))

    def test_station_related_ex(self):
        # this is not a good test but not entirely sure where it is getting its dataset and research projects from
        self.assertIsNotNone(self.station.related_ex())

    def test_station_research_objects(self):
        self.assertIsNotNone(self.station.research_projects())

    def test_station_datasets(self):
        self.assertIsNotNone(self.station.datasets())

    def test_station_uni(self):
        self.assertEquals(unicode(self.station), self.station.name)


