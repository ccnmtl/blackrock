from django.db import models
from datetime import datetime

# Static Lookup Tables
class Audience(models.Model):
  name = models.CharField(max_length=50, unique=True)

  def __unicode__(self):
    return self.name

class DigitalFormat(models.Model):
  name = models.CharField(max_length=50, unique=True)
  def __unicode__(self):
    return self.name

class Keyword(models.Model):
  name = models.CharField(max_length=50)
  facet = models.CharField(max_length=50)
  
  class Meta:
    unique_together = (("name", "facet"),)
  
  def __unicode__(self):
    return self.name
  
class Institution(models.Model):
  name = models.CharField(max_length=50, unique=True)
  
  def __unicode__(self):
    return self.name
  
class LocationSubtype(models.Model):
  name = models.CharField(max_length=50, unique=True)
  
  def __unicode__(self):
    return self.name

class LocationType(models.Model):
  name = models.CharField(max_length=50, unique=True)
  
  def __unicode__(self):
    return self.name
  
class PersonType(models.Model):
  name = models.CharField(max_length=50, unique=True)
  
  def __unicode__(self):
    return self.name
  
class PublicationType(models.Model):
  name = models.CharField(max_length=50, unique=True)
  
  def __unicode__(self):
    return self.name
  
class RegionType(models.Model):
  name = models.CharField(max_length=50, unique=True)

  def __unicode__(self):
    return self.name

class RightsType(models.Model):
  name = models.CharField(max_length=50, unique=True)
  
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
  keyword = models.ManyToManyField(Keyword)

  created_date = models.DateTimeField('created_date', default=datetime.now)
  modified_date = models.DateTimeField('modified_date', default=datetime.now)
  
  def __unicode__(self):
    return "%s (%.6f,%.6f)" % (self.name, self.latitude, self.longitude)
  
class Station(models.Model):
  name = models.CharField(max_length=500)
  description = models.TextField(null=True, blank=True)
  activation_date = models.DateField('activation_date')
  location = models.ManyToManyField(Location)

  audience = models.ManyToManyField(Audience, null=True, blank=True)
  keyword = models.ManyToManyField(Keyword)
  
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
  keyword = models.ManyToManyField(Keyword)
  
  created_date = models.DateTimeField('created_date', default=datetime.now)
  modified_date = models.DateTimeField('modified_date', default=datetime.now)
  
  def __unicode__(self):
    return self.name
  
class Person(models.Model):
  name = models.CharField(max_length=500)
  description = models.TextField(null=True, blank=True)
  person_type = models.ManyToManyField(PersonType, null=True, blank=True)
  institution = models.ManyToManyField(Institution)
  professional_title = models.CharField(max_length=50)
  address = models.TextField(null=True, blank=True)
  phone = models.CharField(max_length=10, null=True, blank=True)
  email = models.EmailField()
  url = models.URLField(null=True, blank=True)
  
  audience = models.ManyToManyField(Audience, null=True, blank=True)
  keyword = models.ManyToManyField(Keyword)
  
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
  keyword = models.ManyToManyField(Keyword)
  location = models.ManyToManyField(Location, null=True, blank=True)
  
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
  keyword = models.ManyToManyField(Keyword)
  location = models.ManyToManyField(Location)
  person = models.ManyToManyField(Person, null=True, blank=True)
  
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
  keyword = models.ManyToManyField(Keyword)
  dataset = models.ManyToManyField(DataSet, null=True, blank=True)
  location = models.ManyToManyField(Location, null=True, blank=True)
  person = models.ManyToManyField(Person, null=True, blank=True)
  
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
  keyword = models.ManyToManyField(Keyword)
  dataset = models.ManyToManyField(DataSet, null=True, blank=True)
  digital_object = models.ManyToManyField(DigitalObject, null=True, blank=True)
  location = models.ManyToManyField(Location, null=True, blank=True)
  person = models.ManyToManyField(Person, null=True, blank=True)
  publication = models.ManyToManyField(Publication, null=True, blank=True)
  
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
  keyword = models.ManyToManyField(Keyword)
  dataset = models.ManyToManyField(DataSet, null=True, blank=True)
  digital_object = models.ManyToManyField(DigitalObject, null=True, blank=True)
  location = models.ManyToManyField(Location, null=True, blank=True)
  person = models.ManyToManyField(Person, null=True, blank=True)
  
  created_date = models.DateTimeField('created_date', default=datetime.now)
  modified_date = models.DateTimeField('modified_date', default=datetime.now)
  
  def __unicode__(self):
    return self.name
  