from blackrock.mammals.management.commands.import_traps import Command, clean_up, read_csv_data, new_expeditions, guess_habitat, guess_bait, create_points, teardown, test_points, test_expedition_ids
from blackrock.mammals.management.commands.import_difficulty import access_difficulty_table, Command

# class TestCommandFunctions(TestCase):

#     #def setUp(self):

#     def test_read_csv_data(self):
#     	self.read_csv = read_csv_data("csv_values.csv")
#         self.assertIsNotNone(self.read_csv)

#     def test_clean_up(self):
#     	self.clean_up = clean_up("csv_values.csv")
#     	self.assertIsNotNone(self.clean_up)

#     def test_new_expeditions(self):
#     	self.new_expedition = 

#     def test_guess_habitat(self):

#     def test_guess_bait(self):

#     def test_new_expeditions(self):




# 58 	0 	def new_expeditions():
# 59 		    """ hardwiring for now """
# 60 	0 	    for eid in test_expedition_ids:
# 61 	0 	        the_new_expedition = Expedition()
# 62 	0 	        the_new_expedition.id = int(eid)
# 63 	0 	        the_new_expedition.start_date_of_expedition = datetime.now()
# 64 	0 	        the_new_expedition.created_on = datetime.now()
# 65 	0 	        the_new_expedition.save()
# 66 		
# 67 		
# 68 	0 	def guess_habitat(values):
# 69 	0 	    label = values['habitat'].lower()
# 70 	0 	    if 'maple mesic' in label:
# 71 	0 	        return Habitat.objects.get(label__icontains='sugar maple')
# 72 	0 	    if 'chestnut' in label:
# 73 	0 	        return Habitat.objects.get(label__icontains='chestnut oak')
# 74 	0 	    if 'maple swamp' in label:
# 75 	0 	        return Habitat.objects.get(label__icontains='maple swamp')
# 76 	0 	    if 'successional' in label:
# 77 	0 	        return Habitat.objects.get(label__icontains='successional')
# 78 	0 	    if 'hickory forest' in label:
# 79 	0 	        return Habitat.objects.get(label__icontains='oak slope')
# 80 		
# 81 		
# 82 	0 	def guess_bait(values):
# 83 		    """
# 84 		            Lure
# 85 		            Marshmallows
# 86 		            Fruit
# 87 		            Peanut butter mix
# 88 		            Meat/Poultry
# 89 		            Fish
# 90 		    """
# 91 		
# 92 	0 	    label = values['bait'].lower()
# 93 	0 	    if 'fish' in label:
# 94 	0 	        return Bait.objects.get(bait_name__icontains='fish')
# 95 	0 	    if 'lure' in label:
# 96 	0 	        return Bait.objects.get(bait_name__icontains='lure')
# 97 	0 	    if 'marshmallows' in label:
# 98 	0 	        return Bait.objects.get(bait_name__icontains='marshmallows')
# 99 	0 	    if 'fruit' in label:
# 100 	0 	        return Bait.objects.get(bait_name__icontains='fruit')
# 101 	0 	    if 'peanut' in label:
# 102 	0 	        return Bait.objects.get(bait_name__icontains='peanut')
# 103 	0 	    if 'meat' in label:
# 104 	0 	        return Bait.objects.get(bait_name__icontains='meat')
# 105 		
# 106 		
# 107 	0 	def create_points(data):
# 108 	0 	    for id, values in data.iteritems():
# 109 	0 	        print values
# 110 	0 	        new_point = TrapLocation()
# 111 	0 	        exp = Expedition.objects.get(id=values['exp_id'])
# 112 		
# 113 	0 	        if exp.grid_square_id is None:
# 114 	0 	            square_coords = values['square_number']
# 115 	0 	            exp.grid_square_id = [
# 116 		                g.id for g in GridSquare.objects.all()
# 117 		                if g.battleship_coords() == square_coords][0]
# 118 		
# 119 	0 	        new_point.expedition = exp
# 120 	0 	        new_point.save()
# 121 	0 	        new_point.expedition.save()
# 122 		
# 123 	0 	        new_point.whether_a_trap_was_set_here = True
# 124 	0 	        new_point.transect_distance = values['distance']
# 125 		
# 126 		        # geography:
# 127 		        # TODO some duplicates inside these model methods here.. can be
# 128 		        # removed.
# 129 	0 	        new_point.set_transect_bearing_wrt_magnetic_north(values['bearing'])
# 130 	0 	        new_point.set_actual_lat_long([values['lat'], values['lon']])
# 131 	0 	        new_point.set_suggested_lat_lon_from_mag_north(
# 132 		            values['bearing'], values['distance'])
# 133 		
# 134 	0 	        new_point.understory = values['understory']
# 135 	0 	        new_point.student_names = values['student_name']
# 136 	0 	        new_point.team_letter = values['team_name']
# 137 	0 	        new_point.team_number = values['trap_number']
# 138 	0 	        new_point.bait_still_there = (values['bait_left'] == 't')
# 139 		
# 140 	0 	        if values['animal']:
# 141 	0 	            species = Species.objects.get(
# 142 		                common_name__icontains=values['animal'])
# 143 	0 	            animal = Animal()
# 144 	0 	            animal.species = species
# 145 	0 	            animal.save()
# 146 	0 	            new_point.animal = animal
# 147 	0 	            animal.save()
# 148 		
# 149 	0 	        if values['habitat'] is not None:
# 150 	0 	            habitat = guess_habitat(values)
# 151 	0 	            new_point.habitat_id = habitat.id
# 152 		
# 153 	0 	        if values['bait'] is not None:
# 154 	0 	            bait = guess_bait(values)
# 155 	0 	            new_point.bait_id = bait.id
# 156 		
# 157 	0 	        new_point.save()
# 158 	0 	        test_points.append(new_point)
# 159 		
# 160 		
# 161 	0 	def teardown():
# 162 		    """so we can try multiple iterations of this"""
# 163 	0 	    for e in Expedition.objects.filter(id__in=test_expedition_ids):
# 164 	0 	        for p in e.traplocation_set.all():
# 165 	0 	            p.delete()
# 166 	0 	        e.delete()
# 167 		
# 168 	0 	    for p in test_points:
# 169 	0 	        p.delete()
# 170 		
# 171 	0 	    for t in TrapLocation.objects.filter(expedition=None):
# 172 	0 	        t.delete()