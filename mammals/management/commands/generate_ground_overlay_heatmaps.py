from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import  * 
from django.contrib.gis.measure import D # D is a shortcut for Distance 
from django.utils import simplejson
from csv import reader, excel_tab
from datetime import datetime, date
from blackrock.mammals.heatmap import heatmap

import sys
import pdb


from blackrock.mammals.models import *

class Command(BaseCommand):
    """Based on http://jjguy.com/heatmap/"""
    def handle(self, *app_labels, **options):
        for h in Habitat.objects.all():
            h.ground_overlay_heatmap()
        for s in Species.objects.all():
            s.ground_overlay_heatmap()



def test_heatmap():
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
   
