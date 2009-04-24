from django.contrib.gis.db import models

#class Location(models.Model):
#  def __unicode__(self):
#    return "(%.2f, %.2f)" % (self.x, self.y)

#  x = models.DecimalField(max_digits=10, decimal_places=2)
#  y = models.DecimalField(max_digits=10, decimal_places=2)

class Tree(models.Model):
  def __str__(self):
    #return "Tree %d (%.2fcm %s at (%.2f,%.2f))" % (self.id, self.dbh, self.species, self.location)
    return "Tree %d" % self.id

  #class Admin:
  #  list_display = ('id', 'dbh', 'species', 'location')

  id = models.IntegerField(primary_key=True)
  species = models.CharField(max_length=100)
  dbh = models.DecimalField(max_digits=10, decimal_places=2)

  #location = models.ForeignKey('Location')

  # location
  #lat = models.DecimalField(max_digits=10, decimal_places=2)
  #lon = models.DecimalField(max_digits=10, decimal_places=2)  

  # GeoDjango specific
  location = models.PointField()
  objects = models.GeoManager()  


#class Plot(models.Model):
#  name = models.CharField(max_length=100)
#  trees = ForeignKey(Tree)