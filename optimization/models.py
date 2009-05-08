from django.contrib.gis.db import models
from django.db import connection

class Plot(models.Model):
  def __unicode__(self):
    return self.name

  name = models.CharField(max_length=100)
  
  # stored calculations
  area = models.DecimalField(max_digits=10, decimal_places=2)   # area in square meters
  density = models.DecimalField(max_digits=10, decimal_places=2, null=True)# population density
  basal = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # basal area
  
  # GIS layer
  NE_corner = models.PointField()
  objects = models.GeoManager()
  
  def update(self):
    # calculate and store population density, basal area
    self.area = 40000
    self.density = str(self.tree_set.count() * 10000.0 / self.area)

    tablename = Tree._meta.db_table
    dbh_field = Tree._meta.get_field('dbh').column
    plot_field = Tree._meta.get_field('plot').column

    cursor = connection.cursor()

    sqlcmd = """SELECT SUM(%s) FROM "%s" WHERE "%s" = '%s'
             """ % (dbh_field, tablename, plot_field, self.id) 

    cursor.execute(sqlcmd)
    summation = cursor.fetchone()[0] or 0.0

    temp = float(summation) * 0.785398
    self.basal = str(temp / self.area)

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