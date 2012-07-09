from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import  * 
from django.contrib.gis.measure import D # D is a shortcut for Distance 
from django.utils import simplejson
import pdb
#this is just a very long string:
from blackrock.mammals.management.commands.grid_json import grid_json
from blackrock.mammals.models import *

class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        #GridPoint.objects.all().delete()
        #GridSquare.objects.all().delete()
        all_points = []
        grid_obj = simplejson.loads(grid_json)
        label_int = 0        
        for row_obj in grid_obj:
            for square_obj in row_obj:
                label_int += 1
                sw, nw, ne, se, center  = square_obj
                new_square = GridSquare()
                new_square.SW_corner = GridPoint.create(sw)
                new_square.NW_corner = GridPoint.create(nw)
                new_square.NE_corner = GridPoint.create(ne)
                new_square.SE_corner = GridPoint.create(se)
                new_square.center    = GridPoint.create(center)
                new_square.use_existing_points()
                new_square.label = label_int
                new_square.save()
                
        print "Squares added:"
        print len (GridSquare.objects.all())
        print "Points added:"
        print len (GridPoint.objects.all())
        
