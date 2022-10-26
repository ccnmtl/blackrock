from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
# from django.db.models import Avg # not yet
from django.db import connection
from django.db.models import Manager


class Plot(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)

    # stored calculations
    # area in square meters
    area = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(
        max_digits=10, decimal_places=2)  # width of plot in meters (x axis)
    height = models.DecimalField(
        max_digits=10, decimal_places=2)  # height of plot in meters (y axis)
    # population density
    density = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # basal area
    basal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    num_species = models.IntegerField(null=True)
    mean_dbh = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    variance_dbh = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)

    # GIS layer
    NW_corner = models.PointField(default=Point())
    objects = Manager()

    def precalc(self):
        # calculate and store population density, basal area, other values
        # self.area = 40000   # TODO calculate? -- being passed in right now
        self.density = str(self.tree_set.count() * 10000.0 / float(self.area))

        num_trees = self.tree_set.count()

        tablename = Tree._meta.db_table
        dbh_field = Tree._meta.get_field('dbh').column
        species_field = Tree._meta.get_field('species').column
        plot_field = Tree._meta.get_field('plot').column

        cursor = connection.cursor()

        sqlcmd = (
            'SELECT COUNT(DISTINCT '  # nosec
            '%s) FROM "%s" WHERE "%s" = \'%s\''  # nosec
            % (species_field, tablename, plot_field, self.id)  # nosec
        )

        cursor.execute(sqlcmd)
        self.num_species = cursor.fetchone()[0] or 0

        sqlcmd = (
            'SELECT SUM(%s) FROM "%s" WHERE "%s" = \'%s\''  # nosec
            % (dbh_field, tablename, plot_field, self.id)  # nosec
        )

        cursor.execute(sqlcmd)
        summation = cursor.fetchone()[0] or 0.0

        temp = float(summation) * 0.785398
        self.basal = str(temp / float(self.area))

        self.mean_dbh = summation / num_trees
        # self.mean_dbh =
        # self.tree_set.objects.aggregate(Avg('dbh'))['dbh__avg']  # not yet

        sql = 'SELECT SUM((%s-%s)^2) FROM "%s" WHERE "%s" = \'%s\''  # nosec
        cmd = sql % (dbh_field, self.mean_dbh, tablename, plot_field, self.id)

        cursor.execute(cmd)
        variance_temp = cursor.fetchone()[0] or 0.0
        if num_trees > 0:
            self.variance_dbh = str(variance_temp / (num_trees))
        else:
            self.variance_dbh = 0

        self.save()
        # return super(Plot, self).save(*args, **kwargs)
        return


class Tree(models.Model):

    def __str__(self):
        # return "Tree %d (%.2fcm %s at (%.2f,%.2f))" % (self.id, self.dbh,
        # self.species, self.location)
        return "Tree %d" % self.id

    id = models.IntegerField(primary_key=True)
    species = models.CharField(max_length=100)
    dbh = models.DecimalField(max_digits=10, decimal_places=2)

    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)

    # GIS layer
    location = models.PointField(default=Point())
    objects = Manager()
