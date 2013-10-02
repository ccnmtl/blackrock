from blackrock.mammals.models import *
from django.test import TestCase
from blackrock.mammals.grid_math import to_lat_long, set_up_block, \
    positive_radians, degrees_to_radians, length_of_transect, walk_transect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils import simplejson



class ModelsTest(TestCase):

    def setUp(self):
        '''trying to create sighting leaving out attibtutes whic are key or objects - location = objects = species = date = observers =    observation_type =     how_many_observed =      notes ='''
        self.sighting = Sighting()
        self.sighting.save()
        self.expedition = Expedition()
        self.expedition.save()
        self.trap_location = TrapLocation()
        self.trap_location.save()
        self.species = Species(latin_name="official_mouse_name", common_name="blackrock_mouse", about_this_species="too smart for traps",)
        self.species.save()
        self.animal = Animal(species=self.species, description="this is a special mouse", tag_number="6789", health="excellent", weight_in_grams=35) #left off sex of animal, age of animal, scale used - foreign keys? other details which were booleans with default left off
        self.animal.save()
        self.habitat = Habitat(label="habitat label", blurb="this is a habitat", image_path_for_legend="/path/here", color_for_map="111")
        self.habitat.save()
        self.timed_expedition = Expedition(end_date_of_expedition=datetime.now())
        self.timed_expedition.save()
        self.time_trap = TrapLocation(expedition=self.timed_expedition, team_letter="team name here", team_number=6, habitat=self.habitat, animal=self.animal)
        self.time_trap.save()
        self.new_sighting = Sighting(species=self.species, date=datetime.now())
        self.new_sighting.save()
        self.grid_point_nw = GridPoint()
        self.grid_point_nw.save()
        self.grid_point_ne = GridPoint()
        self.grid_point_ne.save()
        self.grid_point_sw = GridPoint()
        self.grid_point_sw.save()
        self.grid_point_se = GridPoint()
        self.grid_point_se.save()
        self.grid_point_center = GridPoint()
        self.grid_point_center.save()
        self.grid_square = GridSquare(NW_corner=self.grid_point_nw, NE_corner=self.grid_point_ne, SW_corner=self.grid_point_sw, SE_corner=self.grid_point_se, center=self.grid_point_center, display_this_square=False, row=1, column=0, access_difficulty=3, terrain_difficulty=4)
        self.grid_square.save()

    def test_sighting_methods(self):
        self.new_sighting.set_lat_long([5.0, 8.0])
        self.assertIsNotNone(self.new_sighting.location)
        self.assertEquals(self.new_sighting.lat(), 5.0)
        # make sure blank sightings returns None
        self.assertEquals(self.sighting.lat(), None)
        self.assertEquals(self.new_sighting.lon(), 8.0)
        self.assertEquals(self.sighting.lon(), None)
        self.assertIsNotNone(self.new_sighting.date_for_solr())

    def test_species_has_attributes(self):
        species_attributes = self.species.dir()
        self.assertIn("latin_name", species_attributes)
        self.assertIn("common_name", species_attributes)
        self.assertIn("about_this_species", species_attributes)
        self.assertEquals(self.species.latin_name, "official_mouse_name")
        self.assertEquals(self.species.common_name, "blackrock_mouse")
        self.assertEquals(self.species.about_this_species, "too smart for traps")
        self.other_species = Species()
        self.other_species.latin_name = "official_name"
        self.other_species.common_name = "blackrock"
        self.other_species.about_this_species = "too smart for traps"
        self.assertEquals(self.other_species.latin_name, "official_name")
        self.assertEquals(self.other_species.common_name, "blackrock")
        self.assertEquals(self.other_species.about_this_species, "too smart for traps")



    def test_grid_point_assignments_dir_and_uni(self):
        self.grid_point_nw.set_lat_long([4,5])
        gp_dir = self.grid_point_nw.dir()
        self.grid_point_nw.save()
        self.assertIn("geo_point", gp_dir)
        self.assertIn("objects", gp_dir)
        self.assertEquals(self.grid_point_nw.lat(), 4.0)
        self.assertEquals(self.grid_point_nw.lon(), 5.0)
        self.assertEquals(self.grid_point_nw.NSlat(), '%0.5F N' % abs(self.grid_point_nw.lat()))
        self.assertEquals(self.grid_point_nw.EWlon(), '%0.5F E' % abs(self.grid_point_nw.lon()))
        self.assertEquals(self.grid_point_nw.gps_coords(),"%s, %s" % (self.grid_point_nw.NSlat(), self.grid_point_nw.EWlon()))
        self.assertEquals(unicode(self.grid_point_nw), self.grid_point_nw.gps_coords() )
        self.assertEquals(type(self.grid_point_nw.create([6,7])), type(GridPoint()))
        self.grid_point_se.set_lat_long([-8,-9])
        self.grid_point_se.save()
        self.assertEquals(self.grid_point_se.NSlat(), '%0.5F S' % abs(self.grid_point_se.lat()))
        self.assertEquals(self.grid_point_se.EWlon(), '%0.5F W' % abs(self.grid_point_se.lon()))
        self.assertEquals(self.grid_point_se.lat(), self.grid_point_se.geo_point.coords[0])
        self.assertEquals(self.grid_point_se.lon(), self.grid_point_se.geo_point.coords[1])


    def test_sighting_has_attributes(self):
        contains = dir(self.sighting)
        self.assertIn("set_lat_long", contains)
        self.assertIn("lat", contains)
        self.assertIn("lon", contains)
        self.assertIn("date_for_solr", contains)


    def test_expedition_has_attributes(self):
        contains = dir(self.expedition)
        self.assertIn("get_absolute_url", contains)
        self.assertIn("how_many_mammals_caught", contains)
        self.assertIn("team_points", contains)
        self.assertIn("set_end_time_if_none", contains)
        self.assertIn("end_minute_string", contains)
        self.assertIn("end_hour_string", contains)
        self.assertIn("set_end_time_from_strings", contains)
        self.assertIn("transects_json", contains)

    def test_expedition_dir(self):
        contains = self.expedition.dir()
        self.assertIn("get_absolute_url", contains)
        self.assertIn("how_many_mammals_caught", contains)
        self.assertIn("team_points", contains)
        self.assertIn("set_end_time_if_none", contains)
        self.assertIn("end_minute_string", contains)
        self.assertIn("end_hour_string", contains)
        self.assertIn("set_end_time_from_strings", contains)
        self.assertIn("transects_json", contains)


    def test_trap_location_has_attributes(self):
        contains = dir(self.trap_location)
        self.assertIn("create_from_obj", contains)
        self.assertIn("recreate_point_obj", contains)
        self.assertIn("date", contains)
        self.assertIn("date_for_solr", contains)
        self.assertIn("trap_nickname", contains)
        self.assertIn("transect_endpoints", contains)
        self.assertIn("set_transect_bearing_wrt_magnetic_north", contains)
        self.assertIn("transect_bearing_wrt_magnetic_north", contains)
        self.assertIn("set_suggested_lat_long", contains)
        self.assertIn("set_actual_lat_long", contains)

    def test_trap_location_date_none(self):
        no_date = self.trap_location.date()
        self.assertIsNone(no_date)
        no_date_solr = self.trap_location.date_for_solr()
        self.assertIsNone(no_date_solr)

    def test_trap_location_date_exists(self):
        date = self.time_trap.date()
        self.assertIsNotNone(date)
        date_solr = self.time_trap.date_for_solr()
        self.assertIsNotNone(date_solr)

    def test_trap_location_nickname(self):
        team_nickname = self.time_trap.trap_nickname()
        self.assertEquals(team_nickname, self.time_trap.team_letter + str(self.time_trap.team_number))

    def test_trap_location_species(self):
        species_does_not_exist = self.trap_location.species_if_any()
        self.assertIsNone(species_does_not_exist)
        has_species = self.time_trap.species_if_any()
        self.assertIsNotNone(has_species)
        self.assertEquals(has_species, "blackrock_mouse")

    def test_trap_location_habitat(self):
        no_habitat = self.trap_location.habitat_if_any()
        self.assertIsNone(no_habitat)
        has_habitat = self.time_trap.habitat_if_any()
        self.assertIsNotNone(has_habitat)
        self.assertEquals(has_habitat, "habitat label")

    def test_habitat_id(self):
        no_habitat_id = self.trap_location.habitat_id_if_any()
        self.assertIsNone(no_habitat_id)
        has_habitat_id = self.time_trap.habitat_id_if_any()
        self.assertIsNotNone(has_habitat_id)


    def test_trap_location_dir(self):
        dir_test = self.time_trap.dir()
        self.assertIn("habitat_if_any", dir_test)
        self.assertIn("habitat_id_if_any", dir_test)
        self.assertIn("species_if_any", dir_test)


    def test_create_observation_type(self):
        observation = ObservationType()
        self.failUnlessEqual(type(ObservationType()), type(observation))

    def test_create_observation_self(self):
        self.observation = ObservationType()
        self.observation.save()
        self.failUnlessEqual(type(ObservationType()), type(self.observation))

    def test_grid_square_uni_dir(self):
        self.assertEquals(unicode(self.grid_square), "Row %d, column %d" % (self.grid_square.row, self.grid_square.column))
        dir_test = self.grid_square.dir()
        self.assertIn("row", dir_test)
        self.assertIn("column", dir_test)
        self.assertIn("access_difficulty", dir_test)
        self.assertIn("corner_names", dir_test)
        self.assertIn("corners", dir_test)
        self.assertIn("corner_obj", dir_test)
        self.assertIn("corner_obj_json", dir_test)
        self.assertIn("info_for_display", dir_test)
        self.assertIn("block_json", dir_test)

    def test_grid_square_corner_names_method(self):
        corner_names = self.grid_square.corner_names()
        self.assertEquals(['SW_corner','NW_corner','NE_corner','SE_corner','center'], corner_names)

    def test_battleship_coords(self):
        battleship_coordinates = self.grid_square.battleship_coords()
        self.assertIsNotNone(battleship_coordinates)

#    def test_grid_square_display_info(self):
#        info_for_display = self.grid_square.info_for_display()
        #self.assertIn("row", info_for_display)
        #self.assertIn("column", info_for_display)
        #self.assertIn("access_difficulty", info_for_display)
        #self.assertIn("terrain_difficulty", info_for_display)
        #self.assertIn("database_id", info_for_display)



    def tearDown(self):
        self.sighting.delete()
        self.expedition.delete()
        self.trap_location.delete()
        self.timed_expedition.delete()
        self.time_trap.delete()



#     suggested_point = models.PointField(null=True, blank=True)

#     actual_point = models.PointField(null=True, blank=True)
#     objects = models.GeoManager()

#     # instead we're linking directly to the type of trap.
#     trap_type = models.ForeignKey(
#         TrapType, null=True, blank=True,
#         help_text="Which type of trap, if any, was left at this location.")

#     understory = models.TextField(
#         blank=True, null=True, default='', help_text="Understory")

#     notes_about_location = models.TextField(
#         blank=True, help_text="Notes about the location")

#     # this is wrt true north. for wrt mag. north, see method below
#     transect_bearing = models.FloatField(
#         blank=True, null=True, help_text="Heading of this bearing")
#     transect_distance = models.FloatField(
#         blank=True, null=True, help_text="Distance along this bearing")

#     # Team info:

#     order = models.IntegerField(
#         blank=True, null=True, help_text="Order in which to show this trap.")



#     # info about the outcome:
#     whether_a_trap_was_set_here = models.BooleanField(
#         help_text='''We typically won't use all the locations suggested by the
#         randomization recipe; this denotes that a trap was actually placed at
#         or near this point.''')
#     bait = models.ForeignKey(
#         Bait, null=True, blank=True, help_text="Any bait used",
#         on_delete=models.SET_NULL)
#     animal = models.ForeignKey(Animal, null=True, blank=True,
#                                help_text="Any animals caught",
#                                on_delete=models.SET_NULL)
#     bait_still_there = models.BooleanField(
#         help_text='''Was the bait you left in the trap still there
#         when you came back?''')

#     notes_about_outcome = models.TextField(
#         blank=True, help_text="Any miscellaneous notes about the outcome")

#     student_names = models.TextField(
#         blank=True, null=True,
#         help_text='''Names of the students responsible for this location
#         (this would be filled in, if at all, by the instructor after the
#         students have left the forest.''', max_length=256)



# class TrapLocation(models.Model):

#     @classmethod
#     def create_from_obj(self, transect_obj, point_obj, the_expedition):
#         t = TrapLocation()

#         t.expedition = the_expedition

#         t.transect_bearing = transect_obj['heading']
#         t.team_letter = transect_obj['team_letter']

#         t.set_actual_lat_long(point_obj['point'])
#         t.set_suggested_lat_long(point_obj['point'])
#         t.transect_distance = point_obj['distance']
#         t.team_number = point_obj['point_id']

#         t.save()

#         return t

#     def recreate_point_obj(self):
#         result = {}
#         result['distance'] = self.transect_distance
#         result['point_id'] = self.team_number
#         result['point'] = [self.suggested_lat(), self.suggested_lon()]
#         return result

#     """ A location you might decide to set a trap."""


#     def __unicode__(self):
#         return self.gps_coords()





#     def school_if_any(self):
#         if self.expedition.school:
#             return self.expedition.school.name
#         else:
#             return None

#     def search_map_repr(self):
#         result = {}

#         info_string = \
#             "Animal: %s</br>Habitat: %s</br>School: %s</br>Date: %s" % (
#                 self.species_if_any(), self.habitat_if_any(),
#                 self.school_if_any(), self.date())

#         result['name'] = info_string
#         result['where'] = [self.actual_lat(), self.actual_lon()]

#         result['species'] = self.species_if_any()
#         result['habitat_id'] = self.habitat_id_if_any()
#         result['habitat'] = self.habitat_if_any()
#         result['school'] = self.school_if_any()
#         result['date'] = self.date()

#         return result

#     def dir(self):
#         return dir(self)

#     def gps_coords(self):
#         return "%s, %s" % (self.actual_NSlat(), self.actual_EWlon())







# class Expedition (models.Model):

#     def __unicode__(self):
#         return u"Expedition %d started on %s" % (
#             self.id, self.start_date_of_expedition.strftime("%m/%d/%y"))

#     def get_absolute_url(self):
#         return "/mammals/expedition/%i/" % self.id

#     # TODO make default sort by date, starting w/ most recent.

#     class Meta:
#         ordering = ['-end_date_of_expedition']

#     @classmethod
#     def create_from_obj(self, json_obj, creator):
#         expedition = Expedition()
#         expedition.created_by = creator
#         expedition.number_of_students = 0
#         expedition.save()

#         for transect in json_obj:
#             for point in transect['points']:
#                 TrapLocation.create_from_obj(transect, point, expedition)

#         return expedition

#     start_date_of_expedition = models.DateTimeField(
#         auto_now_add=True, null=True)
#     end_date_of_expedition = models.DateTimeField(
#         auto_now_add=True, null=True)
#     real = models.BooleanField(
#         default=True, help_text="Is this expedition real or just a test?")
#     created_on = models.DateTimeField(auto_now_add=True, null=False)
#     created_by = models.ForeignKey(
#         User, blank=True, null=True, related_name='expeditions_created')
#     notes_about_this_expedition = models.TextField(
#         blank=True, help_text="Notes about this expedition")
#     school = models.ForeignKey(School, blank=True, null=True)
#     school_contact_1_name = models.CharField(
#         blank=True, help_text="First contact @ the school -- name",
#         max_length=256)
#     school_contact_1_phone = models.CharField(
#         blank=True, help_text="First contact @ the school -- e-mail",
#         max_length=256)
#     school_contact_1_email = models.CharField(
#         blank=True, help_text="First contact @ the school -- phone",
#         max_length=256)
#     number_of_students = models.IntegerField(
#         help_text="How many students participated", default=0)
#     grade_level = models.ForeignKey(GradeLevel, null=True, blank=True)
#     grid_square = models.ForeignKey(
#         GridSquare, null=True, blank=True, related_name="Grid Square",
#         verbose_name="Grid Square used for this expedition")

#     field_notes = models.CharField(blank=True, null=True, max_length=1024)
#     cloud_cover = models.ForeignKey(
#         ExpeditionCloudCover, null=True, blank=True,
#         related_name="exp_cloudcover")
#     overnight_temperature = models.ForeignKey(
#         ExpeditionOvernightTemperature, null=True, blank=True,
#         related_name="exp_temperature")

#     overnight_temperature_int = models.IntegerField(
#         help_text="Overnight Temperature", default=0)

#     overnight_precipitation = models.ForeignKey(
#         ExpeditionOvernightPrecipitation, null=True, blank=True,
#         related_name="exp_precipitation")
#     overnight_precipitation_type = models.ForeignKey(
#         ExpeditionOvernightPrecipitationType, null=True, blank=True,
#         related_name="exp_precipitation_type")
#     moon_phase = models.ForeignKey(
#         ExpeditionMoonPhase, null=True, blank=True,
#         related_name="exp_moon_phase")
#     illumination = models.ForeignKey(
#         Illumination, null=True, blank=True, related_name="exp_illumination")


#     def how_many_mammals_caught(self):
#         return len(self.animal_locations())

#     def animal_locations(self):
#         return [t for t in self.trap_locations_ordered_by_team() if t.animal]

#     def trap_locations_ordered_by_team(self):
#         return self.traplocation_set.order_by(
#             'team_number').order_by('team_letter')

#     def team_points(self, team_letter):
#         return [p for p in self.traplocation_set.all().order_by('team_number')
#                 if p.team_letter == team_letter]

#     def set_end_time_if_none(self):
#         if self.end_date_of_expedition is None:
#             self.end_date_of_expedition = datetime.now()
#             self.save()

#     def end_minute_string(self):

#         return "%02d" % self.end_date_of_expedition.minute

#     def end_hour_string(self):
#         return "%02d" % self.end_date_of_expedition.hour

#     def set_end_time_from_strings(self,
#                                   expedition_hour_string,
#                                   expedition_minute_string):
#         self.set_end_time_if_none()
#         new_time = self.end_date_of_expedition.replace(
#             hour=int(expedition_hour_string),
#             minute=int(expedition_minute_string))
#         self.end_date_of_expedition = new_time
#         self.save()

#     def transects(self):
#         result = []
#         points_and_letters = dict((t, t.team_letter)
#                                   for t in self.traplocation_set.all())
#         team_letters = sorted(list(set(points_and_letters.values())))
#         the_id = 0
#         for letter in team_letters:
#             the_other_id = 0
#             the_id = the_id + 1
#             the_points = [
#                 point for point, x in points_and_letters.iteritems()
#                 if x == letter]
#             a_point = the_points[0]
#             transect_points = [a.recreate_point_obj() for a in the_points]

#             for p in transect_points:
#                 the_other_id = the_other_id + 1
#                 p['transect_id'] = the_id
#                 p['point_index_2'] = the_other_id

#             side_of_square = 250.0  # meters. #TODO move this to settings.
#             trig_radians_angle = positive_radians(
#                 degrees_to_radians(a_point.transect_bearing))
#             transect_length = length_of_transect(
#                 trig_radians_angle, side_of_square)

#             magnetic_north = a.transect_bearing_wrt_magnetic_north()

#             transect_info = {
#                 'transect_id': the_id,
#                 'team_letter': letter,
#                 'heading': a_point.transect_bearing,
#                 'heading_radians': trig_radians_angle,
#                 'length': transect_length,
#                 'edge': a_point.transect_endpoints()['edge'],
#                 'heading_wrt_magnetic_north': magnetic_north,
#                 'points': transect_points,
#             }
#             result.append(transect_info)
#         return result

#     def transects_json(self):
#         return simplejson.dumps(self.transects())


