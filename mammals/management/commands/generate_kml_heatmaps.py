from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import  * 
from django.contrib.gis.measure import D # D is a shortcut for Distance 
from django.utils import simplejson
from csv import reader, excel_tab
from datetime import datetime, date
from blackrock.mammals.management.commands.heatmap import Heatmap
from blackrock.mammals.management.commands.colorschemes import *

import sys
import pdb


from blackrock.mammals.models import *

class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        for h in Habitat.objects.all():
            h.kml_heatmap()
        for s in Species.objects.all():
            s.kml_heatmap()
        #test_heatmap()
        


def test_heatmap():
    print "hi"
    the_points = [
        (41.40, -74.00),
        (41.40, -74.03),
        (41.41, -74.03)
    ]
    
    base_path = "mammals/media/kml/test"
    img_test_path    = 'mammals/media/images/heatmaps/'
    img_mammals_path = 'mammals/media/images/heatmaps/mammals/'
    img_species_path = 'mammals/media/images/heatmaps/species/'
    
    
    print "%stest.png" % img_test_path
    hm = Heatmap()  
    hm.heatmap(the_points, "%stest.png" % img_test_path)
   
