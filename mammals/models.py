from django.db import models
from datetime import datetime
from pagetree.models import PageBlock, Section
from django.conf import settings
from django.contrib.gis.db import models
from django.template import Context
from django.template.loader import get_template
from django.db.models.signals import pre_save
from django.contrib.gis.geos import  * 
from django.contrib.gis.measure import D # D is a shortcut for Distance 

class GridPoint(models.Model):
    """ A point in the grid used to sample the forest. Each square is defined by four points. Since it is a grid, a point can be part of up to four different squares, which violates DRY. So I'm denormalizing."""
    
    geo_point = models.PointField(null=True, blank=True)
    objects = models.GeoManager()
    
    @classmethod
    def create(self, coords):
        p = GridPoint()
        p.set_lat_long(coords)
        p.save()
        return p
    
    def set_lat_long (self, coords):
        self.geo_point = "POINT(%s %s)" % (coords[0], coords[1])
        
    def __unicode__(self):
        return self.gps_coords()
   
    def gps_coords(self):
        return "%s, %s" % (self.NSlat(), self.EWlon())
   
    def NSlat(self):
        lat = self.lat()
        if lat > 0:
            return '%0.5F N' % abs(lat)
        return '%0.5F S' % abs(lon)
        
    def EWlon(self):
        lon = self.lon()
        if lon < 0:
            return '%0.5F W' % abs(lon)
        return '%0.5F E' % abs(lon)
        
    def lat(self):
        return self.geo_point.coords[0]
        
    def lon(self):
        return self.geo_point.coords[1]
    
    def close_points (self, meters=0.5):
        """Points less than 50 cm away are pretty darn close for this particular application."""
        candidates = GridPoint.objects.filter(geo_point__distance_lte=(self.geo_point,D(m=meters))) 
        return [ p for p in candidates if p != self]

    def existing_equivalent_point (self):
        existing_close_points = self.close_points()
        if len (existing_close_points) == 0:
            return None
        else:
            return existing_close_points [0]
         

class GridSquare (models.Model):
    """ A square in the grid used to sample the forest. Each square has four points. Contiguous squares will, obviously, have points in common."""

    NW_corner = models.ForeignKey(GridPoint, null=False, blank=False, related_name = "square_to_my_SE", verbose_name="Northwest corner")
    NE_corner = models.ForeignKey(GridPoint, null=False, blank=False, related_name = "square_to_my_SW", verbose_name="Northeast corner")
    SW_corner = models.ForeignKey(GridPoint, null=False, blank=False, related_name = "square_to_my_NE", verbose_name="Southwest corner")
    SE_corner = models.ForeignKey(GridPoint, null=False, blank=False, related_name = "square_to_my_NW", verbose_name="Southeast corner")
    center    = models.ForeignKey(GridPoint, null=False, blank=False, related_name = "square_i_am_in",  verbose_name="Center point")
    
    display_this_square = models.BooleanField() #don't show all the squares
    
    def __unicode__(self):
        return "Row %d, column %d" % (self.row,self.column) 
    
    row = models.IntegerField() 
    column = models.IntegerField() 
    
    access_difficulty = models.IntegerField(help_text = 'This is the Terrain Difficulty, not to be confused with the Access Difficulty, which we are stillnot keeping track of.', verbose_name="Terrain Difficulty") 
    
    #this is arbitrary, just to start out with.
    label = models.IntegerField(help_text = 'This was just an arbitrary number.')
    
    #this will contain the labels from the map given to me by Khoi:
    label_2 = models.IntegerField(help_text = 'This is the number we used in a first numbering. Squares with no number on that map just have a -1.' , verbose_name="Square number on purple map")
    
    @classmethod
    def corner_names(self):
        """ A square has five corners. Deal with it."""
        return ['SW_corner',
                'NW_corner',
                'NE_corner',
                'SE_corner',
                'center']
    
    def corners(self):
        return [ getattr(self, corner_name) for corner_name in self.corner_names()]
        
    def corner_obj (self):
        """ just the lat long coordinates for the corners."""
        return [[c.lat(), c.lon()] for c in self.corners()]
    
    def info_for_display (self):
        result = {}
        result['corner_obj'] = self.corner_obj()
        result['label']   = self.label_2
        result['row']        = self.row
        result['column']     = self.column
        result['access_difficulty']     = self.access_difficulty
        return result
    
        
    def use_existing_points(self):
        """If my point is redundant, use a point that's already in the DB and remove my redundant point."""
        for corner_name in self.corner_names():
            point_to_use_instead = getattr(self, corner_name).existing_equivalent_point()
            if point_to_use_instead:
                getattr(self, corner_name).delete()
                setattr(self, corner_name, point_to_use_instead)
        

        
    
    
    
    # settings.ACCESS_DIFFICULTY_LEVELS
