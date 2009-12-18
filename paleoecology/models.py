from django.db import models
#import math
#from time import time

# one "slice" of the core, containing multiple samples of pollen
class CoreSample(models.Model):
  def __unicode__(self):
    return str(self.depth)

  depth = models.DecimalField(max_digits=8, decimal_places=2)  # depth in cm
  # age?
  # specimens?
  
class PollenType(models.Model):
  name = models.CharField(max_length=100, null=False, unique=True)

  def __unicode__(self):
    return self.name

  POLLEN_TYPES = (
    ('A', 'Tree or shrub'),
    ('B', 'Herb'),
    ('F', 'Fern'),
    ('Q', 'Aquatic (water) plant'),
    ('S', 'Spore'),
    
  )  
  
  type = models.CharField(max_length=1, choices=POLLEN_TYPES)
  
class PollenSample(models.Model):
  core_sample = models.ForeignKey(CoreSample)
  pollen = models.ForeignKey(PollenType)

  def __unicode__(self):
    return "%s cm: %s grains of %s (%s%%)" % (self.core_sample.depth, self.count or 0, self.pollen.name, self.percentage or 0)
   
  percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
  count = models.DecimalField(max_digits=5, decimal_places=2, null=True)