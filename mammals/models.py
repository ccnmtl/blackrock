from django.db import models
from datetime import datetime
from pagetree.models import PageBlock, Section
from django.conf import settings
from django.contrib.gis.db import models
from django.template import Context
from django.template.loader import get_template
from django.db.models.signals import pre_save
from django.contrib.gis.geos import  *
from django.contrib.gis.measure import D
from django.contrib.auth.models import User

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

         
    def dir(self):
        return dir(self)

class GradeLevel (models.Model):

    def __unicode__(self):
        return self.label
    label =  models.CharField(blank=True, help_text = "The name of the grade level", max_length = 256)

    def dir(self):
        return dir(self)

class Bait (models.Model):

    def __unicode__(self):
        return self.bait_name
    bait_name =  models.CharField(blank=True, help_text = "Label for the type of bait", max_length = 256)
    class Meta:
        verbose_name = "Bait type used"
        verbose_name_plural = "Types of bait used"


    def dir(self):
        return dir(self)
        
        
class Species(models.Model):

    def __unicode__(self):
        return self.common_name
        
    latin_name =  models.CharField(blank=True, help_text = "Binomial species name", max_length = 256)
    common_name =  models.CharField(blank=True, help_text = "Common name", max_length = 512)
    about_this_species =  models.TextField(blank=True, help_text = "A blurb with info about this species at Blackrock")

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species" # http://en.wikipedia.org/wiki/Latin_declension#Fifth_declension_.28e.29



    def dir(self):
        return dir(self)


class Animal(models.Model):        
    def __unicode__(self):
        return self.species.common_name
        
    species = models.ForeignKey (Species, null=True, blank=True)
    tag_info =  models.CharField(blank=True, help_text = "Tag info if the animal was tagged", max_length = 256)
    description =  models.TextField(blank=True, help_text = "age / sex / other notes")



class Trap (models.Model):
    def __unicode__(self):
        return self.trap_string
   
    trap_string =  models.CharField(blank=True, help_text = "This should be a unique string to identify each trap.", max_length = 256)

    notes =  models.CharField(blank=True, help_text = "Notes about this trap.", max_length = 256)



    def dir(self):
        return dir(self)
        
        
class Habitat (models.Model):
    
    def __unicode__(self):
        return self.label

    label =  models.CharField(blank=True, help_text = "Short label for this habitat.", max_length = 256)
    blurb =  models.TextField(blank=True, help_text = "Notes about this habitat (for a habitat page).")
    

    def dir(self):
        return dir(self)
    

    
class GridSquare (models.Model):
    """ A square in the grid used to sample the forest. Each square has four points. Contiguous squares will, obviously, have points in common."""
    
    #TODO: Possible refactor suggested by Anders:
    #       remove these foreign-keys to GridPoint and just make them
    #       members of this GridSquare object, possibly stored as a 4-sided native-GIS polygon.
    

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
    
    class Meta:
        unique_together = ("row", "column") #, thank you very much.
    
    access_difficulty = models.IntegerField(help_text = 'This is the Terrain Difficulty, not to be confused with the Access Difficulty, which we are still not keeping track of.', verbose_name="Terrain Difficulty") 
    
    #This is unreferenced. #TOTO remove.
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
        result['corner_obj']            = self.corner_obj()
        result['label']                 = self.label_2
        result['row']                   = self.row
        result['column']                = self.column
        result['access_difficulty']     = self.access_difficulty
        result['database_id']           = self.id
        return result
        
    def use_existing_points(self):
        """If my point is redundant, use a point that's already in the DB and remove my redundant point."""
        for corner_name in self.corner_names():
            point_to_use_instead = getattr(self, corner_name).existing_equivalent_point()
            if point_to_use_instead:
                getattr(self, corner_name).delete()
                setattr(self, corner_name, point_to_use_instead)

        
    def dir(self):
        return dir(self)
    
class Expedition (models.Model):

    def __unicode__(self):
        return  u"Expedition started on %s" % ( self.start_date_of_expedition )
  
    #TODO make default sort by date, starting w/ most recent. 
    
    @classmethod
    def create_from_obj(self, json_obj, creator):
        expedition = Expedition()
        expedition.created_by = creator
        expedition.number_of_students = 20
        expedition.save()
        
        for transect in json_obj:
            for point in transect['points']:
                new_trap_location = TrapLocation.create_from_obj(transect, point, expedition)
                
        return expedition

    start_date_of_expedition =      models.DateTimeField(auto_now_add=True, null=True)
    end_date_of_expedition   =      models.DateTimeField(auto_now_add=True, null=True)
    
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    created_by = models.ForeignKey(User,blank=True,null=True, related_name = 'expeditions_created')

    notes_about_this_expedition =  models.TextField(blank=True, help_text = "Notes about this expedition")
    
    school_contact_1_name  =  models.CharField(blank=True,  help_text = "First contact @ the school -- name", max_length = 256)
    school_contact_1_phone  =  models.CharField(blank=True,  help_text = "First contact @ the school -- e-mail", max_length = 256)
    school_contact_1_email  =  models.CharField(blank=True,  help_text = "First contact @ the school   -- phone", max_length = 256)

    school_contact_2_name  =  models.CharField(blank=True,  help_text = "First contact @ the school -- name", max_length = 256)
    school_contact_2_phone  =  models.CharField(blank=True,  help_text = "Second contact @ the school  -- e-mail", max_length = 256)
    school_contact_2_email  =  models.CharField(blank=True,  help_text = "Second contact @ the school  -- phone", max_length = 256)


    number_of_students = models.IntegerField(help_text = "How many students participated")
    grade_level = models.ForeignKey(GradeLevel,  null=True, blank=True)

    grid_square = models.ForeignKey(GridSquare, null=True, blank=True, related_name = "Grid Square", verbose_name="Grid Square used for this expedition")


    def dir(self):
        return dir(self)

    def how_many_mammals_caught(self):
        return len([t for t in self.traplocation_set.all() if t.animal])


    def trap_locations_ordered_by_team(self):
        #import pdb
        #pdb.set_trace()
        return self.traplocation_set.order_by('team_letter')


##################################################
class TrapLocation(models.Model):

    @classmethod
    def create_from_obj(self, transect_obj, point_obj, the_expedition):
        t = TrapLocation()
        
        t.expedition = the_expedition
        t.set_lat_long(point_obj['point'])
        t.transect_bearing = transect_obj['heading']
        t.transect_distance = point_obj['distance']
        t.team_letter = transect_obj['team_letter']
        t.team_number = point_obj['point_id']
        t.save()
        
        return t


    """ A location you might decide to set a trap."""
    expedition = models.ForeignKey (Expedition, null=True, blank=True)
    geo_point = models.PointField(null=True, blank=True)
    objects = models.GeoManager()
    trap_used = models.ForeignKey (Trap, null=True, blank=True, help_text = "Which trap, if any, was left at this location")
    notes_about_location =  models.TextField(blank=True, help_text = "Notes about the location")
    
    transect_bearing =  models.FloatField(blank=True, null=True, help_text = "Heading of this bearing")
    transect_distance =  models.FloatField(blank=True, null=True, help_text = "Distance along this bearing")
    
    
    #Team info:
    team_letter = models.CharField   (blank=True, null=True, help_text = "Name of team responsible for this location.", max_length = 256)
    team_number = models.IntegerField(blank=True, null=True, help_text = "Designates which trap.")
    order       = models.IntegerField(blank=True, null=True, help_text = "Order in which to show this trap.")
    
    habitat = models.ForeignKey (Habitat, null=True, blank=True,  help_text = "What habitat best describes this location?")
    
    #info about the outcome:    
    whether_a_trap_was_set_here = models.BooleanField(help_text = "We typically won't use ALL the locations suggested; this denotes that a trap was actually placed at or near this point.")
    
    bait = models.ForeignKey (Bait, null=True, blank=True ,  help_text = "Any bait used")
    
    animal = models.ForeignKey (Animal, null=True, blank=True,  help_text = "Any animals caught")
    
    bait_still_there = models.BooleanField(help_text = "Was the bait you left in the trap still there when you came back?")
    
    notes_about_outcome =  models.TextField(blank=True, help_text = "Any miscellaneous notes about the outcome")
    
        
    student_names =  models.TextField (blank=True, null=True, help_text = "Names of the students responsible for this location (this would be filled in, if at all, by the instructor after the students have left the forest.", max_length = 256)
    
    
    @classmethod
    def create(self, coords):
        p = TrapLocation()
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

    def dir(self):
        return dir(self)

    

