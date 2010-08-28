from django.db import models
from datetime import datetime
from pagetree.models import PageBlock, Section
from django.contrib.contenttypes import generic
from django import forms
from haystack.query import SearchQuerySet
from django.conf import settings

# Static Lookup Tables
class Audience(models.Model):
  name = models.CharField(max_length=100, unique=True)

  def __unicode__(self):
    return self.name

class DigitalFormat(models.Model):
  name = models.CharField(max_length=100, unique=True)
  def __unicode__(self):
    return self.name

class Facet(models.Model):
  name = models.CharField(max_length=50)
  display_name = models.CharField(max_length=100)
  facet = models.CharField(max_length=50)
  
  asset_facets = ['audience', 'study_type', 'species', 'discipline', 'asset_type', 'infrastructure', 'featured']
  
  class Meta:
    unique_together = (("name", "facet"),)
  
  def __unicode__(self):
    return self.name
  
class Institution(models.Model):
  name = models.CharField(max_length=100, unique=True)
  
  def __unicode__(self):
    return self.name
  
class LocationSubtype(models.Model):
  name = models.CharField(max_length=100, unique=True)
  
  def __unicode__(self):
    return self.name

class LocationType(models.Model):
  name = models.CharField(max_length=100, unique=True)
  
  def __unicode__(self):
    return self.name
  
class PersonType(models.Model):
  name = models.CharField(max_length=100, unique=True)
  
  def __unicode__(self):
    return self.name
  
class PublicationType(models.Model):
  name = models.CharField(max_length=100, unique=True)
  
  def __unicode__(self):
    return self.name
  
class RegionType(models.Model):
  name = models.CharField(max_length=100, unique=True)

  def __unicode__(self):
    return self.name

class RightsType(models.Model):
  name = models.CharField(max_length=100, unique=True)
  
  def __unicode__(self):
    return self.name
  
class Tag(models.Model):
  name = models.CharField(max_length=100, unique=True)
  
  def __unicode__(self):
    return self.name
  
class Url(models.Model):
  name = models.URLField()

  def __unicode__(self):
    return self.name  
  
# Base Assets
class Location(models.Model):
  name = models.CharField(max_length=500)
  description = models.TextField(null=True, blank=True)
  
  location_type = models.ManyToManyField(LocationType, null=True, blank=True)
  location_subtype = models.ManyToManyField(LocationSubtype, null=True, blank=True)
  latitude = models.DecimalField(max_digits=18, decimal_places=10)
  longitude = models.DecimalField(max_digits=18, decimal_places=10)
  
  audience = models.ManyToManyField(Audience, null=True, blank=True)
  facet = models.ManyToManyField(Facet)
  tag = models.ManyToManyField(Tag)

  created_date = models.DateTimeField('created_date', default=datetime.now)
  modified_date = models.DateTimeField('modified_date', default=datetime.now)
  
  def __unicode__(self):
    return "%s (%.6f,%.6f)" % (self.name, self.latitude, self.longitude)
  
class Station(models.Model):
  name = models.CharField(max_length=500)
  description = models.TextField(null=True, blank=True)
  access_means = models.TextField(null=True, blank=True)
  activation_date = models.DateField('activation_date')
  
  location = models.ManyToManyField(Location)
  audience = models.ManyToManyField(Audience, null=True, blank=True)
  facet = models.ManyToManyField(Facet)
  tag = models.ManyToManyField(Tag, null=True, blank=True)
  
  created_date = models.DateTimeField('created_date', default=datetime.now)
  modified_date = models.DateTimeField('modified_date', default=datetime.now)

  def __unicode__(self):
    return self.name
  
class Region(models.Model):
  name = models.CharField(max_length=500)
  description = models.TextField(null=True, blank=True)
  location = models.ManyToManyField(Location, null=True, blank=True)
  region_type = models.ManyToManyField(RegionType)
  
  audience = models.ManyToManyField(Audience, null=True, blank=True)
  facet = models.ManyToManyField(Facet)
  tag = models.ManyToManyField(Tag, null=True, blank=True)
  
  created_date = models.DateTimeField('created_date', default=datetime.now)
  modified_date = models.DateTimeField('modified_date', default=datetime.now)
  
  def __unicode__(self):
    return self.name
  
class Person(models.Model):
  name = models.CharField(max_length=500)
  description = models.TextField(null=True, blank=True)
  person_type = models.ManyToManyField(PersonType)
  institution = models.ManyToManyField(Institution)
  professional_title = models.CharField(max_length=100, null=True, blank=True)
  address = models.TextField(null=True, blank=True)
  phone = models.CharField(max_length=10, null=True, blank=True)
  email = models.EmailField()
  url = models.URLField(null=True, blank=True)
  
  audience = models.ManyToManyField(Audience, null=True, blank=True)
  facet = models.ManyToManyField(Facet)
  tag = models.ManyToManyField(Tag, null=True, blank=True)
  
  created_date = models.DateTimeField('created_date', default=datetime.now)
  modified_date = models.DateTimeField('modified_date', default=datetime.now)
  
  def __unicode__(self):
    return self.name
  
class DigitalObject(models.Model):
  name = models.CharField(max_length=500)
  description = models.TextField(null=True, blank=True)
  digital_format = models.ManyToManyField(DigitalFormat)
  url = models.URLField()
  author = models.ManyToManyField(Person, null=True, blank=True)
  source = models.CharField(max_length=500, null=True, blank=True)
  
  audience = models.ManyToManyField(Audience, null=True, blank=True)
  facet = models.ManyToManyField(Facet)
  location = models.ManyToManyField(Location, null=True, blank=True)
  tag = models.ManyToManyField(Tag, null=True, blank=True)
  
  created_date = models.DateTimeField('created_date', default=datetime.now)
  modified_date = models.DateTimeField('modified_date', default=datetime.now)
  
  def __unicode__(self):
    return self.name
  
class DataSet(models.Model):
  name = models.CharField(max_length=500)
  description = models.TextField(null=True, blank=True)
  collection_start_date = models.DateField()
  collection_end_date = models.DateField(null=True, blank=True)
  rights_type = models.ManyToManyField(RightsType)
  url = models.ManyToManyField(Url, null=True, blank=True)
  spatial_explicit = models.BooleanField(default=False)
  
  audience = models.ManyToManyField(Audience, null=True, blank=True)
  facet = models.ManyToManyField(Facet)
  location = models.ManyToManyField(Location)
  person = models.ManyToManyField(Person, null=True, blank=True)
  tag = models.ManyToManyField(Tag, null=True, blank=True)
  
  created_date = models.DateTimeField('created_date', default=datetime.now)
  modified_date = models.DateTimeField('modified_date', default=datetime.now)
  
  def __unicode__(self):
    return self.name

class Publication(models.Model):
  name = models.CharField(max_length=500, unique=True)
  description = models.TextField(null=True, blank=True)
  publication_date = models.DateField(null=True, blank=True)
  publication_type = models.ManyToManyField(PublicationType)
  rights_type = models.ManyToManyField(RightsType)
  url = models.URLField(null=True, blank=True)
  doi_citation = models.TextField()
  
  audience = models.ManyToManyField(Audience, null=True, blank=True)
  facet = models.ManyToManyField(Facet)
  person = models.ManyToManyField(Person, null=True, blank=True)
  tag = models.ManyToManyField(Tag, null=True, blank=True)
  
  created_date = models.DateTimeField('created_date', default=datetime.now)
  modified_date = models.DateTimeField('modified_date', default=datetime.now)
  
  def __unicode__(self):
    return self.name
  
class ResearchProject(models.Model):
  name = models.CharField(max_length=500)
  description = models.TextField()
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  url = models.URLField(null=True, blank=True)
  
  audience = models.ManyToManyField(Audience, null=True, blank=True)
  dataset = models.ManyToManyField(DataSet, null=True, blank=True)
  digital_object = models.ManyToManyField(DigitalObject, null=True, blank=True)
  facet = models.ManyToManyField(Facet)
  location = models.ManyToManyField(Location, null=True, blank=True)
  person = models.ManyToManyField(Person, null=True, blank=True)
  publication = models.ManyToManyField(Publication, null=True, blank=True)
  tag = models.ManyToManyField(Tag, null=True, blank=True)
  
  created_date = models.DateTimeField('created_date', default=datetime.now)
  modified_date = models.DateTimeField('modified_date', default=datetime.now)
  
  def __unicode__(self):
    return self.name
  
class LearningActivity(models.Model):
  name = models.CharField(max_length=500)
  description = models.TextField(null=True, blank=True)
  author = models.ManyToManyField(Person, related_name="author")
  digital_format = models.ManyToManyField(DigitalFormat)
  url = models.ManyToManyField(Url, null=True, blank=True)
   
  audience = models.ManyToManyField(Audience, null=True, blank=True)
  dataset = models.ManyToManyField(DataSet, null=True, blank=True)
  digital_object = models.ManyToManyField(DigitalObject, null=True, blank=True)
  facet = models.ManyToManyField(Facet)
  location = models.ManyToManyField(Location, null=True, blank=True)
  person = models.ManyToManyField(Person, null=True, blank=True)
  tag = models.ManyToManyField(Tag, null=True, blank=True)
  
  created_date = models.DateTimeField('created_date', default=datetime.now)
  modified_date = models.DateTimeField('modified_date', default=datetime.now)
  
  def __unicode__(self):
    return self.name
  
class AssetList(models.Model):
  pageblocks = generic.GenericRelation(PageBlock, related_name="assetlist_pageblock")
  search_criteria = models.TextField()
  template_file = "portal/assetlist.html"
  display_name = "Asset List"
  show_keywords = models.BooleanField(default=True)
  show_categories = models.BooleanField(default=True)
    
  def pageblock(self):
    return self.pageblocks.all()[0]

  def __unicode__(self):
    return unicode(self.pageblock())

  def needs_submit(self):
    return False
  
  def list_count(self):
    return settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE
  
  @classmethod
  def add_form(self):
    class AddForm(forms.Form):
        search_criteria = forms.CharField(widget=forms.widgets.Textarea(attrs={'cols':'80'}))
        show_keywords = forms.BooleanField()
        show_categories = forms.BooleanField()
    return AddForm()

  @classmethod
  def create(self,request):
    search_criteria = request.POST.get('search_criteria','')
    show_keywords = request.POST.get('show_keywords', '')
    show_categories = request.POST.get('show_categories', '')
    return AssetList.objects.create(search_criteria=search_criteria, show_keywords=show_keywords, show_categories=show_categories)
  
  def edit_form(self):
    class EditForm(forms.Form):
        search_criteria = forms.CharField(widget=forms.widgets.Textarea(attrs={'cols':'80'}),
                                 initial=self.search_criteria)
        show_keywords = forms.BooleanField(initial=self.show_keywords)
        show_categories = forms.BooleanField(initial=self.show_categories)
    return EditForm();
  
  def edit(self,vals,files):
    self.search_criteria = vals.get('search_criteria','')
    self.show_keywords = vals.get('show_keywords','')
    self.show_categories = vals.get('show_categories','')
    self.save()  
      
  def list(self):    
    results = SearchQuerySet()
    for facet in Facet.asset_facets:
        results = results.facet(facet)
    
    types = self.search_criteria.split(';')
    for t in types:
      criteria = t.split(',')
      q = ''
      for c in criteria:
        if len(q):
          q += ' OR '
        q += c.strip()
      results = results.narrow(q)

    return results.order_by("name") 
  
  def search_query(self):
    query = ''
    types = self.search_criteria.split(';')
    for t in types:
      criteria = t.split(',')
      for c in criteria:
        c = c.replace(':', '=')
        query += c.strip() + "&"
      
    return query      