from django.db import models
#import math
#from time import time

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
  def __unicode__(self):
    return "%s,%s" % (self.depth, self.pollen.name)
   
  depth = models.DecimalField(max_digits=8, decimal_places=2)  # depth in cm
  pollen = models.ForeignKey(PollenType)
  percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
  count = models.DecimalField(max_digits=5, decimal_places=2, null=True)
  # age?