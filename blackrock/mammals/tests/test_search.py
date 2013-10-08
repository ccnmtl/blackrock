from django.test import TestCase
from blackrock.mammals.search_sites import *
from blackrock.mammals.search_indexes import *
from datetime import datetime

# class TestSearchFile(TestCase):

#     def setUp(self):
#     	self.search_index = SearchIndex()
#     	self.search_index.save()
#         self.trap_location_index = TrapLocationIndex(self.search_index)#text="tests the trap_locaiton_index", habitat="habitat", school="school", observer_name="observer_name", species_label="species_label", habitat_label="habitat_label", school_label="school_label", lat="lat", lon="lon", date=datetime.now(), observed=False, camera=True, tracks_and_signs=True, unsuccessful=True, asset_type="trap door")
#         self.trap_location_index.save()
#         self.sighting_index = SightingIndex(self.search_index)#text="tests the sighting_index", species_id="species_id", habitat="habitat", school="school",observer_name="observer_name", species_label="species_label", habitat_label="habitat_label", school_label="school_label", lat="lat", lon="lon", date=datetime.now(), trapped_and_released=False, observed=False, camera=True, tracks_and_signs=True, unsuccessful=True, real=True, asset_type="sighting of trap door")
#         self.sighting_index.save()

#     def test_trap_location_get_model(self):
#         self.assertIsInstanceOf(self.trap_locaiton_index.get_model(), TrapLocation())



# def get_model(self):
# 34 	0 	        return TrapLocation
# 35 		
# 36 	1 	    def prepare_species_id(self, obj):
# 37 	0 	        if obj.animal:
# 38 	0 	            return obj.animal.species.id
# 39 		        else:
# 40 	0 	            return None
# 41 		
# 42 	1 	    def prepare_habitat(self, obj):
# 43 	0 	        if obj.habitat:
# 44 	0 	            return obj.habitat.id
# 45 		        else:
# 46 	0 	            return None
# 47 		
# 48 	1 	    def prepare_school(self, obj):
# 49 	0 	        if obj.expedition.school:
# 50 	0 	            return obj.expedition.school.id
# 51 		        else:
# 52 	0 	            return None
# 53 		
# 54 	1 	    def prepare_habitat_label(self, obj):
# 55 	0 	        if obj.habitat:
# 56 	0 	            return obj.habitat.label
# 57 		        else:
# 58 	0 	            return None
# 59 		
# 60 	1 	    def prepare_species_label(self, obj):
# 61 	0 	        if obj.animal:
# 62 	0 	            return obj.animal.species.common_name
# 63 		        else:
# 64 	0 	            return None
# 65 		
# 66 	1 	    def prepare_school_label(self, obj):
# 67 	0 	        if obj.expedition.school:
# 68 	0 	            return obj.expedition.school.name
# 69 		        else:
# 70 	0 	            return None
# 71 		
# 72 	1 	    def prepare_date(self, obj):
# 73 	0 	        return obj.date_for_solr()
# 74 		
# 75 	1 	    def prepare_trapped_and_released(self, obj):
# 76 	0 	        if obj.animal:
# 77 	0 	            return True
# 78 		        else:
# 79 	0 	            return False
# 80 		
# 81 	1 	    def prepare_unsuccessful(self, obj):
# 82 	0 	        if obj.animal:
# 83 	0 	            return False
# 84 		        else:
# 85 	0 	            return True
# 86 		
# 87 	1 	    def prepare_real(self, obj):
# 88 	0 	        return obj.expedition.real
# 89 		
# 90 	1 	    def prepare_observer_name(self, obj):
# 91 	0 	        return obj.student_names
# 92 		
# 93 		    # these are not sightings, so none of these three is applicable:
# 94 	1 	    def prepare_observed(self, obj):
# 95 	0 	        return None
# 96 		
# 97 	1 	    def prepare_camera(self, obj):
# 98 	0 	        return None
# 99 		
# 100 	1 	    def prepare_tracks_and_signs(self, obj):
# 101 	0 	        return None
# 102 		
# 103 	1 	    def prepare_lat(self, obj):
# 104 	0 	        return obj.actual_lat()
# 105 		
# 106 	1 	    def prepare_lon(self, obj):
# 107 	0 	        return obj.actual_lon()
# 108 		
# 109 	1 	    def prepare_asset_type(self, obj):
# 110 	0 	        return obj._meta.object_name
# 111 		