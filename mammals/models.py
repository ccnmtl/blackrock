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
from django.utils import simplejson
from mammals.grid_math import *
import os
from blackrock.mammals.heatmap import heatmap


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


    def ground_overlay_heatmap(self):
        """returns a PNG of the distribution of this habitat in the forest"""
        pts = []
        animals = Animal.objects.filter(species=self)
        for a in animals:
            if len(a.traplocation_set.all()):
                a_place = a.traplocation_set.all()[0]
                pts.append ((a_place.lat(), a_place.lon()))
        if len (pts) > 0:
            hm = heatmap.Heatmap()
            img_species_path = 'mammals/media/images/heatmaps/species/'
            hm.heatmap(pts, "%s%d.png" % (img_species_path, self.id))
           


class LabelMenu (models.Model):    
    def __unicode__(self):
        return self.label
    label =  models.CharField(blank=True, null=True, max_length = 256)

class AnimalSex (LabelMenu): #honi soit qui mal y pense
    pass

class AnimalAge (LabelMenu):
    pass
    
class AnimalScaleUsed (LabelMenu):
    pass

class Animal(models.Model):        
    def __unicode__(self):
        return self.species.common_name
        
    species = models.ForeignKey (Species, null=True, blank=True)
    description =  models.TextField(blank=True, help_text = "age / sex / other notes")

    sex =  models.ForeignKey(AnimalSex, null=True, blank=True, verbose_name="Sex of this animal",  related_name = "animals_this_sex")
    age =  models.ForeignKey(AnimalAge, null=True, blank=True, verbose_name="Age of this animal" ,  related_name = "animals_this_age")
    scale_used =  models.ForeignKey(AnimalScaleUsed, null=True, blank=True, verbose_name="Scale used to weigh this animal",  related_name = "animals_this_scale_used")

    tag_number =  models.CharField(blank=True, null=True, max_length = 256, default = '')
    health  = models.CharField(blank=True, null=True, max_length = 256, default = '')
    weight_in_grams   = models.IntegerField(blank=True, null=True, default = None)
    recaptured  = models.BooleanField(default=False)     
    scat_sample_collected = models.BooleanField(default=False) 
    blood_sample_collected = models.BooleanField(default=False) 
    hair_sample_collected = models.BooleanField(default=False) 
    skin_sample_collected = models.BooleanField(default=False) 
    

    
    def dir(self):
        return dir(self)

class Trap (models.Model):
    """It's a trap!"""
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
    
    def ground_overlay_heatmap(self):
        """returns a png file of the distribution of this habitat in the forest"""
        pts = []
        for p in TrapLocation.objects.filter(habitat=self):
            pts.append ((p.lat(), p.lon()))
        if len (pts) > 0:
            hm = heatmap.Heatmap()
            img_habitat_path = 'mammals/media/images/heatmaps/habitats/'
            hm.heatmap(pts, "%s%d.png" % (img_habitat_path, self.id))
            
    
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
    
    def battleship_coords(self ):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        try:
            b_row    = self.row + 1
            b_column = alphabet[(self.column - 1)]
            return "%d%s" % (b_row , b_column)
        except:
            pass
        return '**'
    
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
    
    def corner_obj_json (self):
        """ just the lat long coordinates for the corners. (json)"""
        return simplejson.dumps (self.corner_obj())
    
    def info_for_display (self):
        result = {}
        result['corner_obj']            = self.corner_obj()
        result['label']                 = self.label_2
        result['row']                   = self.row
        result['column']                = self.column
        result['access_difficulty']     = self.access_difficulty
        result['database_id']           = self.id
        result['battleship_coords']     = self.battleship_coords()
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

    
    
class ExpeditionCloudCover (LabelMenu):
    pass
class ExpeditionOvernightTemperature(LabelMenu):
    pass
class ExpeditionOvernightPrecipitation (LabelMenu):
    pass
class ExpeditionOvernightPrecipitationType (LabelMenu):
    pass
class ExpeditionMoonPhase (LabelMenu):
    pass
class Illumination (LabelMenu):
    pass
class TrapType (LabelMenu):
    pass

    
class Expedition (models.Model):

    def __unicode__(self):
        return  u"Expedition started on %s" % ( self.start_date_of_expedition )
  
    #TODO make default sort by date, starting w/ most recent. 
    
    @classmethod
    def create_from_obj(self, json_obj, creator):
        expedition = Expedition()
        expedition.created_by = creator
        expedition.number_of_students = 0
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
    
        
    school_name  =  models.CharField(blank=True, default = "", help_text = "Name of school", max_length = 256)
    
    school_contact_1_name  =  models.CharField(blank=True,  help_text = "First contact @ the school -- name", max_length = 256)
    school_contact_1_phone  =  models.CharField(blank=True,  help_text = "First contact @ the school -- e-mail", max_length = 256)
    school_contact_1_email  =  models.CharField(blank=True,  help_text = "First contact @ the school   -- phone", max_length = 256)

    school_contact_2_name  =  models.CharField(blank=True,  help_text = "First contact @ the school -- name", max_length = 256)
    school_contact_2_phone  =  models.CharField(blank=True,  help_text = "Second contact @ the school  -- e-mail", max_length = 256)
    school_contact_2_email  =  models.CharField(blank=True,  help_text = "Second contact @ the school  -- phone", max_length = 256)


    number_of_students = models.IntegerField(help_text = "How many students participated", default = 0)
    grade_level = models.ForeignKey(GradeLevel,  null=True, blank=True)

    grid_square = models.ForeignKey(GridSquare, null=True, blank=True, related_name = "Grid Square", verbose_name="Grid Square used for this expedition")

    understory   =  models.CharField(blank=True, null=True,  max_length = 256)
    field_notes  =  models.CharField(blank=True, null=True,  max_length = 1024)

    cloud_cover =  models.ForeignKey(ExpeditionCloudCover, null=True, blank=True,  related_name = "exp_cloudcover")
    overnight_temperature =  models.ForeignKey(ExpeditionOvernightTemperature, null=True, blank=True,  related_name = "exp_temperature")
    overnight_precipitation =  models.ForeignKey(ExpeditionOvernightPrecipitation, null=True, blank=True,  related_name = "exp_precipitation")
    overnight_precipitation_type =  models.ForeignKey(ExpeditionOvernightPrecipitationType, null=True, blank=True,  related_name = "exp_precipitation_type")
    moon_phase    =  models.ForeignKey(ExpeditionMoonPhase, null=True, blank=True,  related_name = "exp_moon_phase")
    illumination  =  models.ForeignKey(Illumination, null=True, blank=True,  related_name = "exp_illumination")
   
    
    def dir(self):
        return dir(self)

    def how_many_mammals_caught(self):
        return len(self.animal_locations())

    def animal_locations(self):
        return [t for t in self.trap_locations_ordered_by_team() if t.animal]

    def trap_locations_ordered_by_team(self):
        return self.traplocation_set.order_by('team_number').order_by('team_letter')

    def team_points (self, team_letter):
        return  [p for p in self.traplocation_set.all().order_by('team_number') if p.team_letter == team_letter]
    



##################################################
class TrapLocation(models.Model):

    @classmethod
    def create_from_obj(self, transect_obj, point_obj, the_expedition):
        t = TrapLocation()
        
        t.expedition = the_expedition
        t.set_actual_lat_long(point_obj['point'])
        t.set_suggested_lat_long(point_obj['point'])
        t.transect_bearing = transect_obj['heading']
        t.transect_distance = point_obj['distance']
        t.team_letter = transect_obj['team_letter']
        t.team_number = point_obj['point_id']
        t.save()
        
        return t


    """ A location you might decide to set a trap."""
    expedition = models.ForeignKey (Expedition, null=True, blank=True)
    
    
    suggested_point = models.PointField(null=True, blank=True)
    
    actual_point    = models.PointField(null=True, blank=True)
    objects = models.GeoManager()
    
    #this will probably be retired:
    #trap_used = models.ForeignKey (Trap, null=True, blank=True, help_text = "Which trap, if any, was left at this location (We may not be needing this info.)")
    
    #instead we're linking directly to the type of trap.
    trap_type  =  models.ForeignKey(TrapType, null=True, blank=True, help_text = "Which type of trap, if any, was left at this location.")
    
    
    notes_about_location =  models.TextField(blank=True, help_text = "Notes about the location")
    
    
    #this is wrt true north. for wrt mag. north, see method below
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
    
    #field notes:
    notes_about_outcome =  models.TextField(blank=True, help_text = "Any miscellaneous notes about the outcome")
    understory   =  models.CharField(blank=True, null=True,  max_length = 256)
    cloud_cover =  models.ForeignKey(ExpeditionCloudCover, null=True, blank=True,  related_name = "trap_cloudcover")
    overnight_temperature =  models.ForeignKey(ExpeditionOvernightTemperature, null=True, blank=True,  related_name = "trap_temperature")
    overnight_precipitation =  models.ForeignKey(ExpeditionOvernightPrecipitation, null=True, blank=True,  related_name = "trap_precipitation")
    overnight_precipitation_type =  models.ForeignKey(ExpeditionOvernightPrecipitationType, null=True, blank=True,  related_name = "trap_precipitation_type")
    moon_phase    =  models.ForeignKey(ExpeditionMoonPhase, null=True, blank=True,  related_name = "trap_moon_phase")
    illumination  =  models.ForeignKey(Illumination, null=True, blank=True,         related_name = "trap_illumination")
    student_names =  models.TextField (blank=True, null=True, help_text = "Names of the students responsible for this location (this would be filled in, if at all, by the instructor after the students have left the forest.", max_length = 256)
    
    
    
    def trap_nickname (self):
        return "%s%d" % (self.team_letter, self.team_number)
    
    def transect_endpoints (self):
        trig_radians_angle = positive_radians(degrees_to_radians(self.transect_bearing))
        side_of_square = 250.0 # meters. #TODO move this to settings.
        transect_length = length_of_transect (trig_radians_angle, side_of_square)
        square_center = self.expedition.grid_square.center
        center_point = [square_center.lat(), square_center.lon()]
        result = {}
        result ['center'] = [square_center.lat(), square_center.lon()]
        result ['edge'  ] = list(walk_transect (center_point, transect_length, trig_radians_angle))
        return result
    
    
    def set_transect_bearing_wrt_magnetic_north(self, mnb):
        result  = mnb + 13.0
        if result < 0:
            result = result + 360.0
        if result > 360.0:
            result = result - 360.0
            
        self.transect_bearing = result
    
    def set_suggested_lat_lon_from_mag_north (self, heading_degrees_from_mag_north, distance):
        self.set_transect_bearing_wrt_magnetic_north(heading_degrees_from_mag_north)
        trig_radians_angle = positive_radians(degrees_to_radians(self.transect_bearing))
        square_center = self.expedition.grid_square.center
        center_point = [square_center.lat(), square_center.lon()]
        suggested_location = list(walk_transect (center_point, distance, trig_radians_angle))
        self.set_suggested_lat_long(suggested_location)
        
        
       
    def transect_bearing_wrt_magnetic_north(self):
        result = self.transect_bearing - 13.0
        if result < 0:
            result = result + 360.0
        return result
    
    
    
    
    
    def set_suggested_lat_long (self, coords):
        # see 
        # https://code.djangoproject.com/attachment/ticket/16778/postgis-adapter-2.patch
        # if this breaks again.
        self.suggested_point = "POINT(%s %s)" % (coords[0], coords[1])
        
    def set_actual_lat_long (self, coords):
        # see 
        # https://code.djangoproject.com/attachment/ticket/16778/postgis-adapter-2.patch
        # if this breaks again.
        self.actual_point    = "POINT(%s %s)" % (coords[0], coords[1])
        
    def __unicode__(self):
        return self.gps_coords()
   
    def suggested_gps_coords(self):
        return "%s, %s" % (self.suggested_NSlat(), self.suggested_EWlon())
        
    def actual_gps_coords(self):
        return "%s, %s" % (self.actual_NSlat(), self.actual_EWlon())
    
    def suggested_NSlat(self):
        lat = self.suggested_lat()
        if lat:
            if lat > 0:
                return '%0.5F N' % abs(lat)
            return '%0.5F S' % abs(lon)
        return None
    def suggested_EWlon(self):
        lon = self.suggested_lon()
        if lon:
            if lon < 0:
                return '%0.5F W' % abs(lon)
            return '%0.5F E' % abs(lon)
        return None
        
    def actual_NSlat(self):
        lat = self.actual_lat()
        if lat:
            if lat > 0:
                return '%0.5F N' % abs(lat)
            return '%0.5F S' % abs(lon)
        return None
    def actual_EWlon(self):
        lon = self.actual_lon()
        if lon:
            if lon < 0:
                return '%0.5F W' % abs(lon)
            return '%0.5F E' % abs(lon)
        return None
            
    def suggested_lat(self):
        if self.suggested_point:
            return self.suggested_point.coords[0]
        return None

    def suggested_lon(self):
        if self.suggested_point:
            return self.suggested_point.coords[1]
        return None


        
    def actual_lat(self):
        if self.actual_point:
            return self.actual_point.coords[0]
        return None
            
    def actual_lon(self):
        if self.actual_point:
            return self.actual_point.coords[1]
        return None

            
    def dir(self):
        return dir(self)
        
        

        
            
    if 1 == 1:
    #these are still called from the map page -- see /sentry/group/1260
    #TODO remove; Now ambiguous.    
                        def gps_coords(self):
                            return "%s, %s" % (self.NSlat(), self.EWlon())
                        def NSlat(self):
                            lat = self.lat()
                            if lat:
                                if lat > 0:
                                    return '%0.5F N' % abs(lat)
                                return '%0.5F S' % abs(lon)
                            return None
                        def EWlon(self):
                            lon = self.lon()
                            if lon:
                                if lon < 0:
                                    return '%0.5F W' % abs(lon)
                                return '%0.5F E' % abs(lon)
                            return None
                        def lat(self):
                            if self.suggested_point:
                                return self.suggested_point.coords[0]
                            return None
                            
                        def lon(self):
                            if self.suggested_point:
                                return self.suggested_point.coords[1]
                            return None


def whether_this_user_can_see_mammals_module_data_entry (a_user):
    return a_user != None and len (a_user.groups.filter(name='mammals_module_data_entry')) > 0

