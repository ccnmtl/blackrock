from blackrock.mammals.models import Expedition, Habitat, Bait, TrapLocation, \
    GridSquare, Species, Animal
from csv import reader
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):

    def handle(self, *app_labels, **options):
        INPUT_CSV_FILE_NAME = 'traps_01.csv'
        raw_data = read_csv_data(INPUT_CSV_FILE_NAME)
        clean_data = clean_up(raw_data)
        new_expeditions()
        create_points(clean_data)


test_points = []
test_expedition_ids = []


def read_csv_data(file_name):
    """read the csv data"""
    data = reader(open(file_name))
    fields = next(data)
    result = {}
    for row in data:
        items = zip(fields, row)
        line = dict((k, v.strip()) for k, v in items)
        the_id = int(line['id'])
        if line['exp_id'] not in test_expedition_ids:
            test_expedition_ids.append(line['exp_id'])

        result[the_id] = {}
        for k in fields:
            result[the_id][k] = line[k]
    return result


def clean_up(data):
    categories = ['bait', 'animal', 'habitat', 'understory', 'square_number',
                  'student_name', 'team_name', 'bait_left']

    for the_id, values in data.iteritems():
        for k in categories:
            values[k] = values[k].strip()
            if values[k] == '':
                values[k] = None
        for k in ['bearing', 'distance', 'trap_number', 'exp_id']:
            values[k] = int(values[k])
        for k in ['lat', 'lon']:
            values[k] = float(values[k])
        for k in ['', 'id']:
            del values[k]
    return data


def new_expeditions():
    """ hardwiring for now """
    for eid in test_expedition_ids:
        the_new_expedition = Expedition()
        the_new_expedition.id = int(eid)
        the_new_expedition.start_date_of_expedition = timezone.now()
        the_new_expedition.created_on = timezone.now()
        the_new_expedition.save()


def guess_habitat(values):
    label = values['habitat'].lower()
    if 'maple mesic' in label:
        return Habitat.objects.get(label__icontains='sugar maple')
    if 'chestnut' in label:
        return Habitat.objects.get(label__icontains='chestnut oak')
    if 'maple swamp' in label:
        return Habitat.objects.get(label__icontains='maple swamp')
    if 'successional' in label:
        return Habitat.objects.get(label__icontains='successional')
    if 'hickory forest' in label:
        return Habitat.objects.get(label__icontains='oak slope')


def guess_bait(values):
    """
            Lure
            Marshmallows
            Fruit
            Peanut butter mix
            Meat/Poultry
            Fish
    """

    label = values['bait'].lower()
    if 'fish' in label:
        return Bait.objects.get(bait_name__icontains='fish')
    if 'lure' in label:
        return Bait.objects.get(bait_name__icontains='lure')
    if 'marshmallows' in label:
        return Bait.objects.get(bait_name__icontains='marshmallows')
    if 'fruit' in label:
        return Bait.objects.get(bait_name__icontains='fruit')
    if 'peanut' in label:
        return Bait.objects.get(bait_name__icontains='peanut')
    if 'meat' in label:
        return Bait.objects.get(bait_name__icontains='meat')


def create_points(data):
    for id, values in data.iteritems():
        print(values)
        new_point = TrapLocation()
        exp = Expedition.objects.get(id=values['exp_id'])

        if exp.grid_square_id is None:
            square_coords = values['square_number']
            exp.grid_square_id = [
                g.id for g in GridSquare.objects.all()
                if g.battleship_coords() == square_coords][0]

        new_point.expedition = exp
        new_point.save()
        new_point.expedition.save()

        new_point.whether_a_trap_was_set_here = True
        new_point.transect_distance = values['distance']

        # geography:
        # TODO some duplicates inside these model methods here.. can be
        # removed.
        new_point.set_transect_bearing_wrt_magnetic_north(values['bearing'])
        new_point.set_actual_lat_long([values['lat'], values['lon']])
        new_point.set_suggested_lat_lon_from_mag_north(
            values['bearing'], values['distance'])

        new_point.understory = values['understory']
        new_point.student_names = values['student_name']
        new_point.team_letter = values['team_name']
        new_point.team_number = values['trap_number']
        new_point.bait_still_there = (values['bait_left'] == 't')

        if values['animal']:
            species = Species.objects.get(
                common_name__icontains=values['animal'])
            animal = Animal()
            animal.species = species
            animal.save()
            new_point.animal = animal
            animal.save()

        if values['habitat'] is not None:
            habitat = guess_habitat(values)
            new_point.habitat_id = habitat.id

        if values['bait'] is not None:
            bait = guess_bait(values)
            new_point.bait_id = bait.id

        new_point.save()
        test_points.append(new_point)


def teardown():
    """so we can try multiple iterations of this"""
    for e in Expedition.objects.filter(id__in=test_expedition_ids):
        for p in e.traplocation_set.all():
            p.delete()
        e.delete()

    for p in test_points:
        p.delete()

    for t in TrapLocation.objects.filter(expedition=None):
        t.delete()
