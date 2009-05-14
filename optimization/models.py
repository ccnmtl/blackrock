from django.contrib.gis.db import models
#from django.db.models import Avg # not yet
from django.db import connection

class Plot(models.Model):
  def __unicode__(self):
    return self.name

  name = models.CharField(max_length=100)
  
  # stored calculations
  area = models.DecimalField(max_digits=10, decimal_places=2)   # area in square meters
  density = models.DecimalField(max_digits=10, decimal_places=2, null=True)# population density
  basal = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # basal area
  num_species = models.IntegerField(null=True)
  mean_dbh = models.DecimalField(max_digits=10, decimal_places=2, null=True)
  variance_dbh = models.DecimalField(max_digits=10, decimal_places=2, null=True)
  
  # GIS layer
  NE_corner = models.PointField()
  objects = models.GeoManager()
  
  def precalc(self):
    # calculate and store population density, basal area, other values
    #self.area = 40000   # TODO calculate? -- being passed in right now
    self.density = str(self.tree_set.count() * 10000.0 / float(self.area))

    num_trees = self.tree_set.count()

    tablename = Tree._meta.db_table
    dbh_field = Tree._meta.get_field('dbh').column
    species_field = Tree._meta.get_field('species').column
    plot_field = Tree._meta.get_field('plot').column

    cursor = connection.cursor()

    sqlcmd = """SELECT COUNT(DISTINCT %s) FROM "%s" WHERE "%s" = '%s'
             """ % (species_field, tablename, plot_field, self.id)
             
    cursor.execute(sqlcmd)
    self.num_species = cursor.fetchone()[0] or 0

    sqlcmd = """SELECT SUM(%s) FROM "%s" WHERE "%s" = '%s'
             """ % (dbh_field, tablename, plot_field, self.id) 

    cursor = connection.cursor()
    cursor.execute(sqlcmd)
    summation = cursor.fetchone()[0] or 0.0

    temp = float(summation) * 0.785398
    self.basal = str(temp / float(self.area))
    
    self.mean_dbh = summation / num_trees
    #self.mean_dbh = self.tree_set.objects.aggregate(Avg('dbh'))['dbh__avg']  # not yet
    
    self.variance_dbh = (1 / num_trees-1) * (summation - self.mean_dbh * num_trees)

    self.save()    
    #return super(Plot, self).save(*args, **kwargs)
    return
    

class Tree(models.Model):
  def __unicode__(self):
    #return "Tree %d (%.2fcm %s at (%.2f,%.2f))" % (self.id, self.dbh, self.species, self.location)
    return "Tree %d" % self.id

  id = models.IntegerField(primary_key=True)
  species = models.CharField(max_length=100)
  dbh = models.DecimalField(max_digits=10, decimal_places=2)

  plot = models.ForeignKey(Plot)

  # GIS layer
  location = models.PointField()
  objects = models.GeoManager()  