'''
testing simpler classes
test:
    GradeLevel - uni and dir tested
    Bait - uni and dir - not Meta
    Species - uni and dir - not Meta
    LabelMenu - uni tested
    Animal - uni and dir
    Trap - uni and dir
    Habitat - uni and dir
    School - uni
'''

from django.test import TestCase

from blackrock.mammals.models import Bait, GradeLevel, Species, Animal
from blackrock.mammals.models import LabelMenu, Trap, Habitat, School


class TestMammalModels(TestCase):

    def setUp(self):
        self.grade_level = GradeLevel(label="grade_level_here")
        self.grade_level.save()
        self.bait = Bait(bait_name="very good nibbles")
        self.bait.save()
        self.species = Species(latin_name="official_mouse_name",
                               common_name="blackrock_mouse",
                               about_this_species="too smart for traps",)
        self.species.save()
        self.label_menu = LabelMenu(label="label_here")
        self.label_menu.save()
        #  left off sex of animal, age of animal, scale used
        #  - foreign keys? other details which were booleans
        #  with default left off
        self.animal = Animal(species=self.species,
                             description="this is a special mouse",
                             tag_number="6789",
                             health="excellent",
                             weight_in_grams=35)
        self.animal.save()
        self.trap = Trap(trap_string="ineffective mouse trap",
                         notes="trap has not gotten any mice yet")
        self.trap.save()
        self.habitat = Habitat(label="habitat label",
                               blurb="this is a habitat",
                               image_path_for_legend="/path/here",
                               color_for_map="111")
        self.habitat.save()
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

    def test_grade_level_uni(self):
        gl = self.grade_level.__unicode__()
        self.assertEquals(gl, "grade_level_here")
        self.new_grade_level = GradeLevel()
        self.failUnlessEqual(type(GradeLevel()), type(self.new_grade_level))
        self.failUnless(hasattr(self.new_grade_level, 'label'))
        self.new_grade_level.label = "value of label"
        self.new_grade_level.save()
        self.failUnless(self.new_grade_level.id)
        self.assertEquals(unicode(self.new_grade_level), "value of label")
        self.another_grade_level = GradeLevel()
        self.assertEquals(self.another_grade_level.label, "")

#         try:
#             self.another_grade_level.label = "a" * 267
#             self.another_grade_level.save()
#             self.fail()
#         except DatabaseError:
#             pass  # expected

        self.assertIn("label", self.new_grade_level.dir())

    def test_grade_level_no_self(self):
        new_grade_level = GradeLevel()
        self.failUnlessEqual(type(GradeLevel()), type(new_grade_level))
        self.failUnless(hasattr(new_grade_level, 'label'))
        new_grade_level.label = "value of label"
        new_grade_level.save()
        self.failUnless(new_grade_level.id)
        self.assertEquals(unicode(new_grade_level), "value of label")
        another_grade_level = GradeLevel()
        self.assertEquals(another_grade_level.label, "")

#         try:
#             another_grade_level.label = "a" * 267
#             another_grade_level.save()
#             self.fail()
#         except DatabaseError:
#             pass  # expected

        self.assertIn("label", new_grade_level.dir())

    def test_grade_level_dir(self):
        gl = self.grade_level.dir()
        self.assertEquals(type(gl), list)
        self.assertIn("dir", gl)

    def test_species_uni(self):
        sp_uni = self.species.__unicode__()
        self.assertEquals(sp_uni, "blackrock_mouse")
        self.assertNotEquals(sp_uni, "blkms")
        self.assertIsNot(sp_uni, "blkms")
        self.new_species = Species()
        self.new_species.common_name = "blkms"
        self.assertEquals(unicode(self.new_species), "blkms")

    def test_species_dir(self):
        sp = self.species.dir()
        self.assertEquals(type(sp), list)
        self.assertIn("dir", sp)

    def test_trap_uni(self):
        trap_uni = self.trap.__unicode__()
        self.assertEquals(trap_uni, "ineffective mouse trap")

    def test_trap_dir(self):
        trap_dir = self.trap.dir()
        self.assertEquals(type(trap_dir), list)
        self.assertIn("trap_string", trap_dir)
        self.assertIn("notes", trap_dir)

    def test_bait_uni(self):
        bait_uni = self.bait.__unicode__()
        self.assertEquals(bait_uni, "very good nibbles")
        self.assertEquals(unicode(self.bait), "very good nibbles")
        self.new_bait = Bait()
        self.failUnlessEqual(type(Bait()), type(self.new_bait))
        self.failUnless(hasattr(self.new_bait, "bait_name"))

    def test_bait_dir(self):
        bait_dir = self.bait.dir()
        self.assertEquals(type(bait_dir), list)
        self.assertIn("bait_name", bait_dir)

    def test_label_menu_uni(self):
        label_level_uni = self.label_menu.__unicode__()
        self.assertEquals(label_level_uni, self.label_menu.label)
        self.assertEquals(label_level_uni, "label_here")

    def test_animal_uni_dir(self):
        animal_uni = self.animal.__unicode__()
        self.assertEquals(animal_uni, "blackrock_mouse")
        animal_dir = self.animal.dir()
        self.assertIn("age", animal_dir)

    def test_habitat_uni_dir(self):
        habitat_uni = self.habitat.__unicode__()
        self.assertEquals(habitat_uni, self.habitat.label)
        habitat_dir = self.habitat.dir()
        self.assertIn("label", habitat_dir)
        self.assertIn("blurb", habitat_dir)
        self.assertIn("image_path_for_legend", habitat_dir)
        self.assertIn("color_for_map", habitat_dir)

    def test_school_uni(self):
        school_uni = self.school.__unicode__()
        self.assertEquals(school_uni, self.school.name)
        self.new_school = School()
        self.new_school.name = "new school"
        self.assertEquals(unicode(self.new_school), "new school")
