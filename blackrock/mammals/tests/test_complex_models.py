from blackrock.mammals.models import Species, Animal, Sighting
from blackrock.mammals.models import GridPoint, Expedition, Habitat
from blackrock.mammals.models import TrapLocation, ObservationType, School
from blackrock.mammals.models import GridSquare
from django.test import TestCase
from django.utils import timezone


class TestMoreMammalModels(TestCase):
    def setUp(self):
        ''' trying to create sighting leaving out attibtutes whic are
        key or objects - location = objects = species = date = observers
        =    observation_type =     how_many_observed =      notes ='''
        self.sighting = Sighting()
        self.sighting.save()
        self.expedition = Expedition()
        self.expedition.save()
        # objects = models.GeoManager()
        self.trap_location = TrapLocation(
            expedition=self.expedition,
            notes_about_location="Notes about the location",
            team_letter='C',
            whether_a_trap_was_set_here=True,
            bait_still_there=False,
            notes_about_outcome='This is a good place for a trap.',
            student_names='Student 1, Student 2, Student 3')
        self.trap_location.save()
        self.species = Species(latin_name="official_mouse_name",
                               common_name="blackrock_mouse",
                               about_this_species="too smart for traps",)
        self.species.save()
        # left off sex of animal, age of animal, scale used - foreign keys?
        #  other details which were booleans with default left off
        self.animal_1 = Animal(species=self.species,
                               description="this is a special mouse",
                               tag_number="6789", health="excellent",
                               weight_in_grams=35)
        self.animal_1.save()
        # left off sex of animal, age of animal, scale used - foreign
        # keys? other details which were booleans with default left off
        self.animal_2 = Animal(species=self.species,
                               description="this is a naughty mouse",
                               tag_number="8355", health="excellent",
                               weight_in_grams=45)
        self.animal_2.save()
        # left off sex of animal, age of animal, scale used - foreign keys?
        # other details which were booleans with default left off
        self.animal_3 = Animal(species=self.species,
                               description="this is a super mouse",
                               tag_number="8888", health="excellent",
                               weight_in_grams=15)
        self.animal_3.save()
        self.another_expedition = Expedition(
            start_date_of_expedition=timezone.now(),
            end_date_of_expedition=timezone.now())
        self.another_expedition.save()
        self.habitat = Habitat(label="habitat label",
                               blurb="this is a habitat",
                               image_path_for_legend="/path/here",
                               color_for_map="111")
        self.habitat.save()
        self.trap_1 = TrapLocation(expedition=self.another_expedition,
                                   team_letter="A", team_number=1,
                                   whether_a_trap_was_set_here=True,
                                   bait_still_there=False,
                                   habitat=self.habitat,
                                   animal=self.animal_1)
        self.trap_1.save()
        self.trap_2 = TrapLocation(expedition=self.another_expedition,
                                   team_letter="B", team_number=2,
                                   whether_a_trap_was_set_here=True,
                                   bait_still_there=False,
                                   habitat=self.habitat,
                                   animal=self.animal_2)
        self.trap_2.save()
        self.trap_3 = TrapLocation(expedition=self.another_expedition,
                                   team_letter="C", team_number=3,
                                   whether_a_trap_was_set_here=True,
                                   bait_still_there=False,
                                   habitat=self.habitat,
                                   animal=self.animal_3)
        self.trap_3.save()
        self.trap_4 = TrapLocation(expedition=self.another_expedition,
                                   team_letter="D", team_number=4,
                                   whether_a_trap_was_set_here=True,
                                   bait_still_there=False,
                                   habitat=self.habitat)
        self.trap_4.save()
        self.another_expedition.save()
        self.timed_expedition = Expedition(
            end_date_of_expedition=timezone.now())
        self.timed_expedition.save()
        self.time_trap = TrapLocation(expedition=self.timed_expedition,
                                      team_letter="team name here",
                                      team_number=6, habitat=self.habitat,
                                      whether_a_trap_was_set_here=True,
                                      bait_still_there=False,
                                      animal=self.animal_1)
        self.time_trap.save()
        self.new_sighting = Sighting(species=self.species,
                                     date=timezone.now())
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
        self.grid_square = GridSquare(
            NW_corner=self.grid_point_nw,
            NE_corner=self.grid_point_ne,
            SW_corner=self.grid_point_sw,
            SE_corner=self.grid_point_se,
            center=self.grid_point_center,
            display_this_square=False,
            row=1,
            column=0,
            access_difficulty=3,
            terrain_difficulty=4)
        self.grid_square.save()

    def test_sighting_methods(self):
        self.new_sighting.set_lat_long([5.0, 8.0])
        self.assertIsNotNone(self.new_sighting.location)
        self.assertEqual(self.new_sighting.lat(), 5.0)
        # make sure blank sightings returns None
        self.assertEqual(self.sighting.lat(), None)
        self.assertEqual(self.new_sighting.lon(), 8.0)
        self.assertEqual(self.sighting.lon(), None)
        self.assertIsNotNone(self.new_sighting.date_for_solr())

    def test_species_has_attributes(self):
        species_attributes = self.species.dir()
        self.assertIn("latin_name", species_attributes)
        self.assertIn("common_name", species_attributes)
        self.assertIn("about_this_species", species_attributes)
        self.assertEqual(self.species.latin_name, "official_mouse_name")
        self.assertEqual(self.species.common_name, "blackrock_mouse")
        self.assertEqual(self.species.about_this_species,
                         "too smart for traps")
        self.other_species = Species()
        self.other_species.latin_name = "official_name"
        self.other_species.common_name = "blackrock"
        self.other_species.about_this_species = "too smart for traps"
        self.assertEqual(self.other_species.latin_name,
                         "official_name")
        self.assertEqual(self.other_species.common_name,
                         "blackrock")
        self.assertEqual(self.other_species.about_this_species,
                         "too smart for traps")

    def test_grid_point_assignments_dir_and_uni(self):
        self.grid_point_nw.set_lat_long([4, 5])
        gp_dir = self.grid_point_nw.dir()
        self.grid_point_nw.save()
        self.assertIn("geo_point", gp_dir)
        self.assertIn("objects", gp_dir)
        self.assertEqual(self.grid_point_nw.lat(), 4.0)
        self.assertEqual(self.grid_point_nw.lon(), 5.0)
        self.assertEqual(self.grid_point_nw.NSlat(),
                         '%0.5F N' % abs(self.grid_point_nw.lat()))
        self.assertEqual(self.grid_point_nw.EWlon(),
                         '%0.5F E' % abs(self.grid_point_nw.lon()))
        self.assertEqual(self.grid_point_nw.gps_coords(),
                         "%s, %s" % (self.grid_point_nw.NSlat(),
                                     self.grid_point_nw.EWlon()))
        self.assertEqual(str(self.grid_point_nw),
                         self.grid_point_nw.gps_coords())
        self.assertEqual(type(self.grid_point_nw.create([6, 7])),
                         type(GridPoint()))
        self.grid_point_se.set_lat_long([-8, -9])
        self.grid_point_se.save()
        self.assertEqual(self.grid_point_se.NSlat(),
                         '%0.5F S' % abs(self.grid_point_se.lat()))
        self.assertEqual(self.grid_point_se.EWlon(),
                         '%0.5F W' % abs(self.grid_point_se.lon()))
        self.assertEqual(self.grid_point_se.lat(),
                         self.grid_point_se.geo_point.coords[0])
        self.assertEqual(self.grid_point_se.lon(),
                         self.grid_point_se.geo_point.coords[1])

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
        the_date = self.trap_location.date()
        self.assertIsNotNone(the_date)
        the_date_solr = self.trap_location.date_for_solr()
        self.assertIsNotNone(the_date_solr)

    def test_trap_location_date_exists(self):
        date = self.time_trap.date()
        self.assertIsNotNone(date)
        date_solr = self.time_trap.date_for_solr()
        self.assertIsNotNone(date_solr)

    def test_trap_location_nickname(self):
        team_nickname = self.time_trap.trap_nickname()
        self.assertEqual(team_nickname,
                         (self.time_trap.team_letter +
                          str(self.time_trap.team_number)))

    def test_trap_location_species(self):
        species_does_not_exist = self.trap_location.species_if_any()
        self.assertIsNone(species_does_not_exist)
        has_species = self.time_trap.species_if_any()
        self.assertIsNotNone(has_species)
        self.assertEqual(has_species, "blackrock_mouse")

    def test_trap_location_habitat(self):
        no_habitat = self.trap_location.habitat_if_any()
        self.assertIsNone(no_habitat)
        has_habitat = self.time_trap.habitat_if_any()
        self.assertIsNotNone(has_habitat)
        self.assertEqual(has_habitat, "habitat label")

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
        self.assertEqual(type(ObservationType()), type(observation))

    def test_create_observation_self(self):
        self.observation = ObservationType()
        self.observation.save()
        self.assertEqual(type(ObservationType()), type(self.observation))

    def test_grid_square_uni_dir(self):
        self.assertEqual(str(self.grid_square),
                         "Row %d, column %d" % (self.grid_square.row,
                                                self.grid_square.column))
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
        self.assertEqual(
            ['SW_corner', 'NW_corner', 'NE_corner', 'SE_corner', 'center'],
            corner_names)

    '''There may be a typo in the actual program says for
    corner_name may be supposed to be corner_names'''
    # def test_grid_square_corners(self):
    #     #corner_names = self.grid_square.corner_names()
    #     corners = self.grid_square.corners()
    #     self.assertIn( "SW_corner", corners)
    #     self.assertIn( type(GridPoint()), corners)

    def test_corner_obj(self):
        self.grid_point_nw.set_lat_long([4, 5])
        self.grid_point_se.set_lat_long([-8, -9])
        self.grid_point_sw.set_lat_long([-8, -9])
        self.grid_point_ne.set_lat_long([-8, -9])
        self.grid_point_center.set_lat_long([-8, -9])
        corner_objects = self.grid_square.corner_obj()
        self.assertEqual([[-8.0, -9.0], [4.0, 5.0], [-8.0, -9.0],
                          [-8.0, -9.0], [-8.0, -9.0]], corner_objects)

    def test_corner_obj_json(self):
        self.grid_point_nw.set_lat_long([4, 5])
        self.grid_point_se.set_lat_long([-8, -9])
        self.grid_point_sw.set_lat_long([-8, -9])
        self.grid_point_ne.set_lat_long([-8, -9])
        self.grid_point_center.set_lat_long([-8, -9])
        corner_obj_json = self.grid_square.corner_obj_json()
        self.assertIn("[4.0, 5.0]", corner_obj_json)
        self.assertEqual(('[[-8.0, -9.0], [4.0, 5.0], [-8.0, -9.0], '
                          '[-8.0, -9.0], [-8.0, -9.0]]'), corner_obj_json)

    def test_battleship_coords(self):
        battleship_coordinates = self.grid_square.battleship_coords()
        self.assertIsNotNone(battleship_coordinates)

    # Test More Expedition Methods
    def test_trap_locations(self):
        '''Test methods requiring TrapLocations, Animals, and Teams'''
        '''This is not a good test - the unicode returns the gps coordinates
        so it is returning TrapLocation objects but need to verify that they
        have team letter and number'''
        ae = self.another_expedition
        trap_location_team = ae.trap_locations_ordered_by_team()
        self.assertEqual(1, trap_location_team[0].team_number)
        self.assertEqual('A', trap_location_team[0].team_letter)
        self.assertEqual(2, trap_location_team[1].team_number)
        self.assertEqual('B', trap_location_team[1].team_letter)
        self.assertEqual(3, trap_location_team[2].team_number)
        self.assertEqual('C', trap_location_team[2].team_letter)
        self.assertEqual(4, trap_location_team[3].team_number)
        self.assertEqual('D', trap_location_team[3].team_letter)

    def test_mammals(self):
        '''Only return trap locations which have caught an animal.
        In this case the first three as in above method test_trap_locations.
        Should exclude trap 4.'''
        animals_trapped = self.another_expedition.animal_locations()
        self.assertEqual(1, animals_trapped[0].team_number)
        self.assertEqual("blackrock_mouse",
                         animals_trapped[0].animal.species.common_name)
        self.assertEqual('A', animals_trapped[0].team_letter)
        self.assertEqual(2, animals_trapped[1].team_number)
        self.assertEqual('B', animals_trapped[1].team_letter)
        self.assertEqual(3, animals_trapped[2].team_number)
        self.assertEqual('C', animals_trapped[2].team_letter)

    def test_expedition_unicode(self):
        self.assertEqual(
            str(self.another_expedition),
            "Expedition %d started on %s" % (
                self.another_expedition.id,
                self.another_expedition.start_date_of_expedition.strftime(
                    "%m/%d/%y")))

    def test_expedition_absolute_url(self):
        self.assertEqual(
            self.another_expedition.get_absolute_url(),
            "/mammals/expedition/%i/" % self.another_expedition.id)

    def test_number_of_mammals(self):
        number_of_mammals = self.another_expedition.how_many_mammals_caught()
        self.assertEqual(number_of_mammals, 3)

    def test_team_points(self):
        '''Takes a team_letter and returns matching trap locations
        with letter'''
        team_a = self.another_expedition.team_points('A')
        self.assertEqual(team_a[0].team_letter, 'A')
        team_b = self.another_expedition.team_points('B')
        self.assertEqual(team_b[0].team_letter, 'B')
        team_c = self.another_expedition.team_points('C')
        self.assertEqual(team_c[0].team_letter, 'C')

    def test_end_minute_string(self):
        self.new_expedition = Expedition(field_notes="some field notes here")
        self.new_expedition.save()
        end_minute_string = self.new_expedition.end_minute_string()
        self.assertIsNotNone(end_minute_string)
        self.assertEqual(
            end_minute_string,
            "%02d" % self.new_expedition.end_date_of_expedition.minute)

    def test_end_hour_string(self):
        self.new_expedition = Expedition(field_notes="some field notes here")
        self.new_expedition.save()
        end_hour_string = self.new_expedition.end_hour_string()
        self.assertIsNotNone(end_hour_string)
        self.assertEqual(
            end_hour_string,
            "%02d" % self.new_expedition.end_date_of_expedition.hour)

    def test_expedition_set_time_from_strings(self):
        # not sure how to check actual contents of the time,
        # keeps giving type errors
        self.another_expedition.set_end_time_from_strings("5", "45")
        self.assertIsNotNone(self.another_expedition.end_date_of_expedition)

    # Now test TrapLocation methods
    def test_points_trap_location(self):
        self.trap_4.set_suggested_lat_long([4, 5])
        self.trap_4.set_actual_lat_long([6, 7])
        self.trap_4.save()

        actual_lat = self.trap_4.actual_lat()
        actual_lon = self.trap_4.actual_lon()
        self.assertEqual(actual_lat, 6)
        self.assertEqual(actual_lon, 7)

        suggested_lon = self.trap_4.suggested_lon()
        suggested_lat = self.trap_4.suggested_lat()
        self.assertEqual(suggested_lat, 4)
        self.assertEqual(suggested_lon, 5)

    def test_points_trap_location_when_none(self):
        self.assertIsNone(self.time_trap.suggested_lat())
        self.assertIsNone(self.time_trap.suggested_lon())
        self.assertIsNone(self.time_trap.actual_lat())
        self.assertIsNone(self.time_trap.actual_lon())

    def test_trap_location_unicode(self):
        self.assertEqual(str(self.trap_4), self.trap_4.gps_coords())

    def test_trap_location_suggested_gps_coords(self):
        self.assertEqual(
            self.trap_4.suggested_gps_coords(),
            "%s, %s" % (self.trap_4.suggested_NSlat(),
                        self.trap_4.suggested_EWlon()))

    def test_trap_location_actual_gps_coords(self):
        self.assertEqual(
            self.trap_4.actual_gps_coords(),
            "%s, %s" % (self.trap_4.actual_NSlat(),
                        self.trap_4.actual_EWlon()))

    def test_trap_location_suggested_NSlat_EWlon_positive_values(self):
        self.trap_4.set_suggested_lat_long([4, 5])
        self.trap_4.save()
        self.assertEqual(
            self.trap_4.suggested_NSlat(),
            '%0.5F N' % abs(self.trap_4.suggested_lat()))
        self.assertEqual(
            self.trap_4.suggested_EWlon(),
            '%0.5F E' % abs(self.trap_4.suggested_lon()))

    def test_trap_location_suggested_NSlat_EWlon_negative_values(self):
        self.trap_4.set_suggested_lat_long([-3, -4])
        self.trap_4.save()

        self.assertEqual(
            self.trap_4.suggested_NSlat(),
            '%0.5F S' % abs(self.trap_4.suggested_lat()))
        self.assertEqual(
            self.trap_4.suggested_EWlon(),
            '%0.5F W' % abs(self.trap_4.suggested_lon()))

    def test_trap_location_suggested_NSlat_EWlon_None(self):
        self.assertIsNone(self.time_trap.suggested_lat())
        self.assertIsNone(self.time_trap.suggested_lon())

    def test_trap_location_actual_NSlat_EWlon_positve_values(self):
        self.trap_4.set_actual_lat_long([4, 5])
        self.trap_4.save()
        self.assertEqual(
            self.trap_4.actual_NSlat(),
            '%0.5F N' % abs(self.trap_4.actual_lat()))
        self.assertEqual(
            self.trap_4.actual_EWlon(),
            '%0.5F E' % abs(self.trap_4.actual_lon()))

    def test_trap_location_actual_NSlat_EWlon_negative_values(self):
        self.trap_4.set_actual_lat_long([-3, -4])
        self.trap_4.save()

        self.assertEqual(
            self.trap_4.actual_NSlat(),
            '%0.5F S' % abs(self.trap_4.actual_lat()))
        self.assertEqual(
            self.trap_4.actual_EWlon(),
            '%0.5F W' % abs(self.trap_4.actual_lon()))

    def test_trap_location_actual_NSlat_EWlon_None(self):
        self.assertIsNone(self.time_trap.actual_lat())
        self.assertIsNone(self.time_trap.actual_lon())

    def test_trap_location_school(self):
        self.school = School(name="school",
                             address="school address",
                             contact_1_name="contact 1 for school",
                             contact_1_phone="000-000-0000",
                             contact_1_email="contact1@contact1.com",
                             contact_2_name="contact 2 for school",
                             contact_2_phone="111-111-1111",
                             contact_2_email="contact2@contacts.com",
                             notes="this student has appropriate information")
        self.school.save()
        self.another_expedition.school = self.school
        self.assertIsNotNone(self.trap_4.school_if_any())
        self.assertEqual(self.trap_4.school_if_any(), "school")
        self.assertIsNone(self.time_trap.school_if_any())

    def test_sightings_date_for_solr(self):
        self.new_sighting = Sighting(species=self.species, date=timezone.now())
        self.new_sighting.save()
        self.assertIsNotNone(self.new_sighting.date_for_solr())

    def tearDown(self):
        self.sighting.delete()
        self.expedition.delete()
        self.trap_location.delete()
        self.timed_expedition.delete()
        self.time_trap.delete()
