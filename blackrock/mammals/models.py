from blackrock.mammals.grid_math import to_lat_long, set_up_block, \
    positive_radians, degrees_to_radians, length_of_transect, walk_transect
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models import Manager
import json


class GridPoint(models.Model):

    """ A point in the grid used to sample the forest. Each square is defined
    by four points. Since it is a grid, a point can be part of up to four
    different squares, which violates DRY. So I'm denormalizing."""

    geo_point = models.PointField(null=True, blank=True)
    objects = Manager()

    @classmethod
    def create(self, coords):
        p = GridPoint()
        p.set_lat_long(coords)
        p.save()
        return p

    def set_lat_long(self, coords):
        self.geo_point = "POINT(%s %s)" % (coords[0], coords[1])

    def __str__(self):
        return self.gps_coords()

    def gps_coords(self):
        return "%s, %s" % (self.NSlat(), self.EWlon())

    def NSlat(self):
        lat = self.lat()
        if lat > 0:
            return '%0.5F N' % abs(lat)
        return '%0.5F S' % abs(lat)

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

    def __str__(self):
        return self.label
    label = models.CharField(
        blank=True, help_text="The name of the grade level", max_length=256)

    def dir(self):
        return dir(self)


class Bait(models.Model):

    def __str__(self):
        return self.bait_name
    bait_name = models.CharField(
        blank=True, help_text="Label for the type of bait", max_length=256)

    class Meta:
        ordering = ['bait_name']
        verbose_name = "Bait type used"
        verbose_name_plural = "Types of bait used"

    def dir(self):
        return dir(self)


class Species(models.Model):

    def __str__(self):
        return self.common_name

    latin_name = models.CharField(
        blank=True, help_text="Binomial species name", max_length=256)
    common_name = models.CharField(
        blank=True, help_text="Common name", max_length=512)
    about_this_species = models.TextField(
        blank=True,
        help_text="A blurb with info about this species at Blackrock")

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species"
        ordering = ['common_name']

    def dir(self):
        return dir(self)


class LabelMenu(models.Model):

    def __str__(self):
        return self.label
    label = models.CharField(blank=True, null=True, max_length=256)


class AnimalSex (LabelMenu):
    pass


class AnimalAge (LabelMenu):
    pass


class AnimalScaleUsed (LabelMenu):
    pass


class Animal(models.Model):

    def __str__(self):
        return self.species.common_name

    species = models.ForeignKey(
        Species, null=True, blank=True,
        on_delete=models.SET_NULL)
    description = models.TextField(
        blank=True, help_text="age / sex / other notes")

    sex = models.ForeignKey(AnimalSex, null=True, blank=True,
                            verbose_name="Sex of this animal",
                            related_name="animals_this_sex",
                            on_delete=models.SET_NULL)
    age = models.ForeignKey(AnimalAge, null=True, blank=True,
                            verbose_name="Age of this animal",
                            related_name="animals_this_age",
                            on_delete=models.SET_NULL)
    scale_used = models.ForeignKey(
        AnimalScaleUsed, null=True, blank=True,
        verbose_name="Scale used to weigh this animal",
        related_name="animals_this_scale_used",
        on_delete=models.SET_NULL)

    tag_number = models.CharField(
        blank=True, null=True, max_length=256, default='')
    health = models.CharField(
        blank=True, null=True, max_length=256, default='')
    weight_in_grams = models.IntegerField(
        blank=True, null=True, default=None)
    recaptured = models.BooleanField(default=False)
    scat_sample_collected = models.BooleanField(default=False)
    blood_sample_collected = models.BooleanField(default=False)
    hair_sample_collected = models.BooleanField(default=False)
    skin_sample_collected = models.BooleanField(default=False)

    # DO NOT DELETE THE TRAP LOCATION THIS ANIMAL WAS ASSOCIATED WITH.

    def dir(self):
        return dir(self)


class Trap(models.Model):

    """It's a trap!"""

    def __str__(self):
        return self.trap_string

    trap_string = models.CharField(
        blank=True,
        help_text="This should be a unique string to identify each trap.",
        max_length=256)

    notes = models.CharField(
        blank=True, help_text="Notes about this trap.", max_length=256)

    def dir(self):
        return dir(self)


class Habitat(models.Model):

    def __str__(self):
        return self.label

    class Meta:
        ordering = ['label']

    label = models.CharField(
        blank=True, help_text="Short label for this habitat.", max_length=256)
    blurb = models.TextField(
        blank=True, help_text="Notes about this habitat (for a habitat page).")
    image_path_for_legend = models.CharField(
        blank=True,
        help_text="Path to the round colored circle for this habitat",
        max_length=256)

    color_for_map = models.CharField(
        blank=True, max_length=3, help_text="RGB color to use on the map")

    def dir(self):
        return dir(self)


class GridSquare(models.Model):

    """ A square in the grid used to sample the forest.
    Each square has four points. Contiguous squares will,
    obviously, have points in common."""

    # TODO: Possible refactor suggested by Anders:
    #       remove these foreign-keys to GridPoint and just make them
    # members of this GridSquare object, possibly stored as a 4-sided
    # native-GIS polygon.

    NW_corner = models.ForeignKey(GridPoint, null=False, blank=False,
                                  related_name="square_to_my_SE",
                                  verbose_name="Northwest corner",
                                  on_delete=models.CASCADE)
    NE_corner = models.ForeignKey(GridPoint, null=False, blank=False,
                                  related_name="square_to_my_SW",
                                  verbose_name="Northeast corner",
                                  on_delete=models.CASCADE)
    SW_corner = models.ForeignKey(GridPoint, null=False, blank=False,
                                  related_name="square_to_my_NE",
                                  verbose_name="Southwest corner",
                                  on_delete=models.CASCADE)
    SE_corner = models.ForeignKey(GridPoint, null=False, blank=False,
                                  related_name="square_to_my_NW",
                                  verbose_name="Southeast corner",
                                  on_delete=models.CASCADE)
    center = models.ForeignKey(
        GridPoint, null=False, blank=False, related_name="square_i_am_in",
        verbose_name="Center point",
        on_delete=models.CASCADE)

    # don't show all the squares
    display_this_square = models.BooleanField(default=False)

    def __str__(self):
        return "Row %d, column %d" % (self.row, self.column)

    row = models.IntegerField()
    column = models.IntegerField()

    class Meta:
        unique_together = ("row", "column")  # , thank you very much.

    access_difficulty = models.IntegerField(
        help_text='''is the overall difficulty and length of time for a group
        of students to get to the square from the Science Center.''',
        verbose_name="Access Difficulty", default=0)

    terrain_difficulty = models.IntegerField(
        help_text='How rough the terrain is on this square.',
        verbose_name="Terrain Difficulty", default=0)

    def battleship_coords(self):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        try:
            b_row = self.row + 1
            b_column = alphabet[(self.column - 1)]
            return "%d%s" % (b_row, b_column)
        except IndexError:
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
        return [getattr(self, corner_name)
                for corner_name in self.corner_names()]

    def corner_obj(self):
        """ just the lat long coordinates for the corners."""
        return [[c.lat(), c.lon()] for c in self.corners()]

    def corner_obj_json(self):
        """ just the lat long coordinates for the corners. (json)"""
        return json.dumps(self.corner_obj())

    def info_for_display(self):
        result = {}
        result['corner_obj'] = self.corner_obj()
        result['row'] = self.row
        result['column'] = self.column
        result['access_difficulty'] = self.access_difficulty
        result['terrain_difficulty'] = self.terrain_difficulty
        result['database_id'] = self.id
        result['battleship_coords'] = self.battleship_coords()
        return result

    def dir(self):
        return dir(self)

    def block_json(self):
        block_size_in_m = 250.0
        block_height, block_width = to_lat_long(
            block_size_in_m, block_size_in_m)
        bottom_left = self.SW_corner.lat(), self.SW_corner.lon()
        block = set_up_block(bottom_left, block_height, block_width)
        block_json = json.dumps(block)
        return block_json


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

    class Meta:
        ordering = ['label']


class School(models.Model):

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    name = models.CharField(
        blank=True, default="", help_text="Name of school", max_length=256)
    address = models.CharField(
        blank=True, default="", help_text="Name of school", max_length=256)
    contact_1_name = models.CharField(
        blank=True, help_text="First contact @ the school -- name",
        max_length=256)
    contact_1_phone = models.CharField(
        blank=True, help_text="First contact @ the school -- e-mail",
        max_length=256)
    contact_1_email = models.CharField(
        blank=True, help_text="First contact @ the school   -- phone",
        max_length=256)
    contact_2_name = models.CharField(
        blank=True, help_text="First contact @ the school -- name",
        max_length=256)
    contact_2_phone = models.CharField(
        blank=True, help_text="Second contact @ the school  -- e-mail",
        max_length=256)
    contact_2_email = models.CharField(
        blank=True, help_text="Second contact @ the school  -- phone",
        max_length=256)
    notes = models.CharField(
        blank=True, help_text="Any other notes about this school.",
        max_length=256)


class Expedition(models.Model):

    def __str__(self):
        return "Expedition %d started on %s" % (
            self.id, self.start_date_of_expedition.strftime("%m/%d/%y"))

    def get_absolute_url(self):
        return "/mammals/expedition/%i/" % self.id

    # TODO make default sort by date, starting w/ most recent.

    class Meta:
        ordering = ['-end_date_of_expedition']

    @classmethod
    def create_from_obj(self, json_obj, creator):
        expedition = Expedition()
        expedition.created_by = creator
        expedition.number_of_students = 0
        expedition.save()

        for transect in json_obj:
            for point in transect['points']:
                TrapLocation.create_from_obj(transect, point, expedition)

        return expedition

    start_date_of_expedition = models.DateTimeField(
        auto_now_add=True, null=True)
    end_date_of_expedition = models.DateTimeField(
        auto_now_add=True, null=True)
    real = models.BooleanField(
        default=True, help_text="Is this expedition real or just a test?")
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    created_by = models.ForeignKey(
        User, blank=True, null=True, related_name='expeditions_created',
        on_delete=models.SET_NULL)
    notes_about_this_expedition = models.TextField(
        blank=True, help_text="Notes about this expedition")
    school = models.ForeignKey(School, blank=True, null=True,
                               on_delete=models.SET_NULL)
    school_contact_1_name = models.CharField(
        blank=True, help_text="First contact @ the school -- name",
        max_length=256)
    school_contact_1_phone = models.CharField(
        blank=True, help_text="First contact @ the school -- e-mail",
        max_length=256)
    school_contact_1_email = models.CharField(
        blank=True, help_text="First contact @ the school -- phone",
        max_length=256)
    number_of_students = models.IntegerField(
        help_text="How many students participated", default=0)
    grade_level = models.ForeignKey(GradeLevel, null=True, blank=True,
                                    on_delete=models.SET_NULL)
    grid_square = models.ForeignKey(
        GridSquare, null=True, blank=True, related_name="Grid Square+",
        verbose_name="Grid Square used for this expedition",
        on_delete=models.SET_NULL)

    field_notes = models.CharField(blank=True, null=True, max_length=1024)
    cloud_cover = models.ForeignKey(
        ExpeditionCloudCover, null=True, blank=True,
        related_name="exp_cloudcover",
        on_delete=models.SET_NULL)
    overnight_temperature = models.ForeignKey(
        ExpeditionOvernightTemperature, null=True, blank=True,
        related_name="exp_temperature",
        on_delete=models.SET_NULL)

    overnight_temperature_int = models.IntegerField(
        help_text="Overnight Temperature", default=0)

    overnight_precipitation = models.ForeignKey(
        ExpeditionOvernightPrecipitation, null=True, blank=True,
        related_name="exp_precipitation",
        on_delete=models.SET_NULL)
    overnight_precipitation_type = models.ForeignKey(
        ExpeditionOvernightPrecipitationType, null=True, blank=True,
        related_name="exp_precipitation_type",
        on_delete=models.SET_NULL)
    moon_phase = models.ForeignKey(
        ExpeditionMoonPhase, null=True, blank=True,
        related_name="exp_moon_phase",
        on_delete=models.SET_NULL)
    illumination = models.ForeignKey(
        Illumination, null=True, blank=True, related_name="exp_illumination",
        on_delete=models.SET_NULL)

    def dir(self):
        return dir(self)

    def how_many_mammals_caught(self):
        return len(self.animal_locations())

    def animal_locations(self):
        return [t for t in self.trap_locations_ordered_by_team() if t.animal]

    def trap_locations_ordered_by_team(self):
        return self.traplocation_set.order_by(
            'team_number').order_by('team_letter')

    def team_points(self, team_letter):
        return [p for p in self.traplocation_set.all().order_by('team_number')
                if p.team_letter == team_letter]

    def set_end_time_if_none(self):
        if self.end_date_of_expedition is None:
            self.end_date_of_expedition = timezone.now()
            self.save()

    def end_minute_string(self):

        return "%02d" % self.end_date_of_expedition.minute

    def end_hour_string(self):
        return "%02d" % self.end_date_of_expedition.hour

    def set_end_time_from_strings(self,
                                  expedition_hour_string,
                                  expedition_minute_string):
        self.set_end_time_if_none()
        new_time = self.end_date_of_expedition.replace(
            hour=int(expedition_hour_string),
            minute=int(expedition_minute_string))
        self.end_date_of_expedition = new_time
        self.save()

    def transects(self):
        result = []
        points_and_letters = dict((t, t.team_letter)
                                  for t in self.traplocation_set.all())
        team_letters = sorted(list(set(points_and_letters.values())))
        the_id = 0
        for letter in team_letters:
            the_other_id = 0
            the_id = the_id + 1
            the_points = [
                point for point, x in points_and_letters.items()
                if x == letter]
            a_point = the_points[0]
            transect_points = [a.recreate_point_obj() for a in the_points]

            for p in transect_points:
                the_other_id = the_other_id + 1
                p['transect_id'] = the_id
                p['point_index_2'] = the_other_id

            side_of_square = 250.0  # meters. #TODO move this to settings.
            trig_radians_angle = positive_radians(
                degrees_to_radians(a_point.transect_bearing))
            transect_length = length_of_transect(
                trig_radians_angle, side_of_square)

            magnetic_north = a_point.transect_bearing_wrt_magnetic_north()

            transect_info = {
                'transect_id': the_id,
                'team_letter': letter,
                'heading': a_point.transect_bearing,
                'heading_radians': trig_radians_angle,
                'length': transect_length,
                'edge': a_point.transect_endpoints()['edge'],
                'heading_wrt_magnetic_north': magnetic_north,
                'points': transect_points,
            }
            result.append(transect_info)
        return result

    def transects_json(self):
        return json.dumps(self.transects())


class TrapLocation(models.Model):

    @classmethod
    def create_from_obj(self, transect_obj, point_obj, the_expedition):
        t = TrapLocation()

        t.expedition = the_expedition

        t.transect_bearing = transect_obj['heading']
        t.team_letter = transect_obj['team_letter']

        t.set_actual_lat_long(point_obj['point'])
        t.set_suggested_lat_long(point_obj['point'])
        t.transect_distance = point_obj['distance']
        t.team_number = point_obj['point_id']

        t.save()

        return t

    def recreate_point_obj(self):
        result = {}
        result['distance'] = self.transect_distance
        result['point_id'] = self.team_number
        result['point'] = [self.suggested_lat(), self.suggested_lon()]
        return result

    """ A location you might decide to set a trap."""
    expedition = models.ForeignKey(Expedition, null=True, blank=True,
                                   on_delete=models.SET_NULL)

    suggested_point = models.PointField(null=True, blank=True)

    actual_point = models.PointField(null=True, blank=True)
    objects = Manager()

    # instead we're linking directly to the type of trap.
    trap_type = models.ForeignKey(
        TrapType, null=True, blank=True,
        help_text="Which type of trap, if any, was left at this location.",
        on_delete=models.SET_NULL)

    understory = models.TextField(
        blank=True, null=True, default='', help_text="Understory")

    notes_about_location = models.TextField(
        blank=True, help_text="Notes about the location")

    # this is wrt true north. for wrt mag. north, see method below
    transect_bearing = models.FloatField(
        blank=True, null=True, help_text="Heading of this bearing")
    transect_distance = models.FloatField(
        blank=True, null=True, help_text="Distance along this bearing")

    # Team info:
    team_letter = models.CharField(
        blank=True, null=True,
        help_text="Name of team responsible for this location.",
        max_length=256)
    team_number = models.IntegerField(
        blank=True, null=True,
        help_text="Differentiates the traps each team is in charge of.")
    order = models.IntegerField(
        blank=True, null=True, help_text="Order in which to show this trap.")

    habitat = models.ForeignKey(
        Habitat, null=True, blank=True,
        help_text="What habitat best describes this location?",
        on_delete=models.SET_NULL)

    # info about the outcome:
    whether_a_trap_was_set_here = models.BooleanField(
        default=False,
        help_text='''We typically won't use all the locations suggested by the
        randomization recipe; this denotes that a trap was actually placed at
        or near this point.''')
    bait = models.ForeignKey(
        Bait, null=True, blank=True, help_text="Any bait used",
        on_delete=models.SET_NULL)
    animal = models.ForeignKey(Animal, null=True, blank=True,
                               help_text="Any animals caught",
                               on_delete=models.SET_NULL)
    bait_still_there = models.BooleanField(
        default=False,
        help_text='''Was the bait you left in the trap still there
        when you came back?''')

    notes_about_outcome = models.TextField(
        blank=True, help_text="Any miscellaneous notes about the outcome")

    student_names = models.TextField(
        blank=True, null=True,
        help_text='''Names of the students responsible for this location
        (this would be filled in, if at all, by the instructor after the
        students have left the forest.''', max_length=256)

    def date(self):
        if self.expedition and self.expedition.end_date_of_expedition:
            return self.expedition.end_date_of_expedition.strftime("%m/%d/%y")
        else:
            return None

    def date_for_solr(self):
        if self.expedition:
            return self.expedition.end_date_of_expedition
        else:
            return None

    def trap_nickname(self):
        return "%s%d" % (self.team_letter, self.team_number)

    def transect_endpoints(self):
        trig_radians_angle = positive_radians(
            degrees_to_radians(self.transect_bearing))
        side_of_square = 250.0  # meters. #TODO move this to settings.
        transect_length = length_of_transect(
            trig_radians_angle, side_of_square)
        square_center = self.expedition.grid_square.center
        center_point = [square_center.lat(), square_center.lon()]
        result = {}
        result['center'] = [square_center.lat(), square_center.lon()]
        result['edge'] = list(
            walk_transect(center_point, transect_length, trig_radians_angle))
        return result

    def set_transect_bearing_wrt_magnetic_north(self, mnb):
        result = mnb + 13.0
        if result < 0:
            result = result + 360.0
        if result > 360.0:
            result = result - 360.0

        self.transect_bearing = result

    def set_suggested_lat_lon_from_mag_north(self,
                                             heading_degrees_from_mag_north,
                                             distance):
        self.set_transect_bearing_wrt_magnetic_north(
            heading_degrees_from_mag_north)
        trig_radians_angle = positive_radians(
            degrees_to_radians(self.transect_bearing))
        square_center = self.expedition.grid_square.center
        center_point = [square_center.lat(), square_center.lon()]
        suggested_location = list(
            walk_transect(center_point, distance, trig_radians_angle))
        self.set_suggested_lat_long(suggested_location)

    def transect_bearing_wrt_magnetic_north(self):
        result = self.transect_bearing - 13.0
        if result < 0:
            result = result + 360.0
        return result

    def set_suggested_lat_long(self, coords):
        # see
        # https://code.djangoproject.com/attachment/ticket/
        #     16778/postgis-adapter-2.patch
        # if this breaks again.
        self.suggested_point = "POINT(%s %s)" % (coords[0], coords[1])

    def set_actual_lat_long(self, coords):
        # see
        # https://code.djangoproject.com/attachment/ticket/
        #     16778/postgis-adapter-2.patch
        # if this breaks again.
        self.actual_point = "POINT(%s %s)" % (coords[0], coords[1])

    def __str__(self):
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
            return '%0.5F S' % abs(lat)
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
            return '%0.5F S' % abs(lat)
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

    def species_if_any(self):
        if self.animal:
            return self.animal.species.common_name
        else:
            return None

    def habitat_if_any(self):
        if self.habitat:
            return self.habitat.label
        else:
            return None

    def habitat_id_if_any(self):
        if self.habitat:
            return self.habitat.id
        else:
            return None

    def school_if_any(self):
        if self.expedition.school:
            return self.expedition.school.name
        else:
            return None

    def search_map_repr(self):
        result = {}

        info_string = \
            "Animal: %s</br>Habitat: %s</br>School: %s</br>Date: %s" % (
                self.species_if_any(), self.habitat_if_any(),
                self.school_if_any(), self.date())

        result['name'] = info_string
        result['where'] = [self.actual_lat(), self.actual_lon()]

        result['species'] = self.species_if_any()
        result['habitat_id'] = self.habitat_id_if_any()
        result['habitat'] = self.habitat_if_any()
        result['school'] = self.school_if_any()
        result['date'] = self.date()

        return result

    def dir(self):
        return dir(self)

    def gps_coords(self):
        return "%s, %s" % (self.actual_NSlat(), self.actual_EWlon())


class ObservationType (LabelMenu):
    pass


class Sighting(models.Model):
    location = models.PointField(
        null=True, blank=True, help_text="Where the animal was seen")
    objects = Manager()
    species = models.ForeignKey(
        Species, null=True, blank=True, help_text="Best guess at species.",
        on_delete=models.SET_NULL)
    habitat = models.ForeignKey(
        Habitat, null=True, blank=True,
        help_text="What habitat best describes this location?",
        on_delete=models.SET_NULL)
    date = models.DateTimeField(
        auto_now_add=True, null=True, help_text="Where the animal was seen")
    observation_type = models.ForeignKey(
        ObservationType, null=True, blank=True,
        help_text="e.g. sighting, camera-trapped, etc.",
        on_delete=models.SET_NULL)
    observers = models.TextField(
        blank=True, null=True,
        help_text="Initials of the people who made the observation.",
        default=None)
    how_many_observed = models.IntegerField(
        blank=True, null=True,
        help_text="How many animals were observed, if applicable.",
        default=None)
    notes = models.TextField(
        blank=True, null=True, help_text="Notes about the location",
        default=None)

    def set_lat_long(self, coords):
        # see
        # https://code.djangoproject.com/attachment/ticket/
        #     16778/postgis-adapter-2.patch
        # if this breaks again.
        self.location = "POINT(%s %s)" % (coords[0], coords[1])

    def lat(self):
        if self.location:
            return self.location.coords[0]
        return None

    def lon(self):
        if self.location:
            return self.location.coords[1]
        return None

    def date_for_solr(self):
        if self.date:
            return self.date
        else:
            return None


def whether_this_user_can_see_mammals_module_data_entry(a_user):
    return (a_user is not None and
            len(a_user.groups.filter(name='mammals_module_data_entry')) > 0)
