import datetime
from haystack import site
from haystack.indexes import SearchIndex
from haystack.fields import MultiValueField, CharField
from portal.models import *

class AssetIndex(SearchIndex):
  text = CharField(document=True, use_template=True)
  name = CharField(model_attr='name')
  audience = MultiValueField(faceted=True)
  study_type = MultiValueField(faceted=True)
  species = MultiValueField(faceted=True)
  discipline = MultiValueField(faceted=True)
  asset_type = CharField(faceted=True)
  infrastructure = MultiValueField(faceted=True)
  
  def prepare_study_type(self, obj):
    return [facet.display_name for facet in obj.facet.filter(facet='Study Type')]

  def prepare_species(self, obj):
    return [facet.display_name for facet in obj.facet.filter(facet='Species')]

  def prepare_discipline(self, obj):
    return [facet.display_name for facet in obj.facet.filter(facet='Discipline')]
  
  def prepare_audience(self, obj): 
    return [audience.name for audience in obj.audience.all()]
  
  def prepare_infrastructure(self, obj):
    return [facet.display_name for facet in obj.facet.filter(facet='Infrastructure')]
  
  def prepare_asset_type(self, obj):
    return obj._meta.object_name
  
class PersonIndex(AssetIndex):
  person_type = MultiValueField()
  
  def prepare_person_type(self, obj):
    return [p.name for p in obj.person_type.all()]
  
site.register(Location, AssetIndex)
site.register(Station, AssetIndex)
site.register(Region, AssetIndex)
site.register(Person, PersonIndex)
site.register(DataSet, AssetIndex)
site.register(DigitalObject, AssetIndex)
site.register(Publication, AssetIndex)
site.register(ResearchProject, AssetIndex)
site.register(LearningActivity, AssetIndex)

from django.contrib import databrowse

databrowse.site.register(DigitalObject)
databrowse.site.register(Location)
databrowse.site.register(Station)
databrowse.site.register(Person)
databrowse.site.register(DataSet)
databrowse.site.register(Publication)
databrowse.site.register(Region)
databrowse.site.register(ResearchProject)
databrowse.site.register(LearningActivity)
databrowse.site.register(ForestStory)

databrowse.site.register(Audience)
databrowse.site.register(DigitalFormat)
databrowse.site.register(Facet)
databrowse.site.register(Institution)
databrowse.site.register(LocationType)
databrowse.site.register(LocationSubtype)
databrowse.site.register(PersonType)
databrowse.site.register(PublicationType)
databrowse.site.register(RegionType)
databrowse.site.register(RightsType)
databrowse.site.register(Tag)
databrowse.site.register(Url)
