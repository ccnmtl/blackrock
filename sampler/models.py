from django.db import models

class Location(models.Model):
  def __str__(self):
    return "(%.2f, %.2f)" % (self.x, self.y)

  x = models.DecimalField(max_digits=10, decimal_places=2)
  y = models.DecimalField(max_digits=10, decimal_places=2)

class Tree(models.Model):
  def __str__(self):
    return "Tree %d (%.2fcm %s at %s)" % (self.id, self.dbh, self.species, self.location)

  #class Admin:
  #  list_display = ('id', 'dbh', 'species', 'location')

  id = models.IntegerField(primary_key=True)
  species = models.CharField(max_length=100)
  location = models.ForeignKey('Location')
  dbh = models.DecimalField(max_digits=10, decimal_places=2)
  # plot = models.ForeignKey('Plot')

# how to represent years??

#class Plot(models.Model):
#  name = models.CharField(max_length=100)
#  trees = ForeignKey(Tree)
#  year?

# student data... transect
# class Transect
#   start = ForeignKey(Location)
#   end = ForeignKey(Location)
#   trees = ForeignKey(Tree)

