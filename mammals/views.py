from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext, Context, TemplateDoesNotExist
from django.shortcuts import render_to_response
from django.db import connection 
from django.db.models import get_model, DateField
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import management
from django.db.models.fields.related import OneToOneField
import StringIO, sys, urllib
from datetime import datetime, date
from time import strptime
from pagetree.models import Hierarchy
from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import user_passes_test
from decimal import Decimal
from django.utils import simplejson
from django.contrib.gis.geos import  * 
from django.contrib.gis.measure import D # D is a shortcut for Distance 
from django.template.loader import get_template
from mammals.grid_math import *
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, TemplateDoesNotExist
from random import *


def get_float (request, name, default):
    number =request.POST.get(name, default)
    return float (number)


def get_int (request, name, default):
    number =request.POST.get(name, default)
    return int (number)


class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items

        return rendered_func



@rendered_with('mammals/grid.html')
def grid(request):

    #butler library:
    #default_lat = 40.80835;
    #default_lon = -73.96455;
    
    #blackrock
    default_lat = 41.400;
    default_lon = -74.0305;
    
    
    if (request.method != 'POST'):
        magnetic_declination                    = -13.0 # degrees
        grid_center                             = [default_lat, default_lon]
        height_in_blocks,  width_in_blocks,     = [21, 27]
        block_height_in_m, block_width_in_m     = [250.0, 250.0]
        grid_center_y, grid_center_x = grid_center
        
    else:
        magnetic_declination =                  get_float( request, 'magnetic_declination',     -13.0)
        height_in_blocks =                      get_int( request,   'height_in_blocks',         21)
        width_in_blocks   =                     get_int( request,   'width_in_blocks',          27)
        block_height_in_m =                     get_float( request, 'block_height_in_m',        250.0)
        block_width_in_m  =                     get_float( request, 'block_width_in_m',         250.0)
        grid_center_y          =                get_float( request, 'grid_center_y',            default_lat)
        grid_center_x           =               get_float( request, 'grid_center_x',            default_lon)
        grid_center = grid_center_y, grid_center_x
    
    grid_height_in_m = block_height_in_m * height_in_blocks
    grid_width_in_m  = block_width_in_m  * width_in_blocks
    
    block_height, block_width  = to_lat_long (block_height_in_m,  block_width_in_m )
    grid_height,  grid_width   = to_lat_long (grid_height_in_m,   grid_width_in_m  )
    
    grid_bottom,  grid_left  = grid_center[0] - (grid_height / 2), grid_center[1] - (grid_width/2)
    
    grid_json = []
    
    
    for i in range (0, height_in_blocks):
        new_column = []
        for j in range (0, width_in_blocks):
        
            bottom_left = grid_bottom + i * block_height, grid_left + j * block_width
            
            block = set_up_block (bottom_left, block_height, block_width)
            rotated_block = rotate_points (block, grid_center, magnetic_declination)
            
            new_column.append(rotated_block)
            
        grid_json.append (new_column)
    
    return {
        'grid_json': simplejson.dumps(grid_json)
        ,'magnetic_declination'                      :  magnetic_declination # degrees
        ,'grid_center_y'                             :  grid_center_y
        ,'grid_center_x'                             :  grid_center_x
        ,'height_in_blocks'                          :  height_in_blocks
        ,'width_in_blocks'                           :  width_in_blocks
        ,'block_height_in_m'                         :  block_height_in_m
        ,'block_width_in_m'                          :  block_width_in_m
    
    }
    
    
def pick_trap_location (center, max_distance_from_center_y, max_distance_from_center_x, rotate_by):

    result = {}    
    center_meters = to_meters_point (center)
    
    y_distance = uniform(0, abs(max_distance_from_center_y))
    x_distance = uniform(0, abs(max_distance_from_center_x))

    y_direction = choice(['north', 'south'])
    x_direction = choice(['east',  'west'])
    
    
    
    if y_direction == 'south':
        trap_location_y_meters = center_meters[0] + y_distance
        dy =  -y_distance
    else:
        trap_location_y_meters = center_meters[0] - y_distance
        dy =   y_distance
    
    if x_direction == 'west':
        trap_location_x_meters = center_meters[1] + x_distance
        dx = - x_distance
    else:
        trap_location_x_meters = center_meters[1] - x_distance
        dx =   x_distance
    
    
    
    
    point_lat_long_before_rotation = to_lat_long(trap_location_y_meters, trap_location_x_meters)
    
    # the way i have the code written, this converts to meters and back to degrees again.
    # could refactor to increase speed and precision, if needed. probably not.
    
    point_lat_long = rotate_about_a_point (point_lat_long_before_rotation, center, rotate_by)

    result ['point'] =       point_lat_long
    result ['distance_y'] =  y_distance
    result ['distance_x'] =  x_distance
    result ['direction_y'] = y_direction
    result ['direction_x'] = x_direction
    result ['heading']         = radians_to_degrees(atan2(dx, dy))
    result ['actual_distance'] = sqrt( y_distance ** 2 + x_distance ** 2 )
    
    return result
    
@rendered_with('mammals/grid_block.html')
def grid_block(request):

    #butler library:
    #default_lat = 40.80835;
    #default_lon = -73.96455;
    
    #blackrock
    default_lat = 41.400;
    default_lon = -74.0305;
    
    if (request.method != 'POST'):
        magnetic_declination                    = -13.0 # degrees
        block_center                             = [default_lat, default_lon]
        block_height_in_m, block_width_in_m     = [250.0, 250.0]
        selected_block_center_y, selected_block_center_x = block_center
        num_points = 5
        
    else:
        num_points           =                  get_int  ( request, 'num_points',               5 )
        magnetic_declination =                  get_float( request, 'magnetic_declination',     -13.0)
        block_height_in_m =                     get_float( request, 'block_height_in_m',        250.0)
        block_width_in_m  =                     get_float( request, 'block_width_in_m',         250.0)
        selected_block_center_y          =      get_float( request, 'selected_block_center_y',  default_lat)
        selected_block_center_x           =     get_float( request, 'selected_block_center_x',  default_lon)
        block_center = selected_block_center_y, selected_block_center_x
    
    block_height, block_width    = to_lat_long (block_height_in_m,  block_width_in_m )
    
    trap_sites = []
    
    for i in range (num_points):
        center = selected_block_center_y, selected_block_center_x
        loc = pick_trap_location (center, block_height_in_m / 2, block_width_in_m / 2, magnetic_declination)
        loc ['point_id'] = i + 1
        trap_sites.append (loc)
    
    bottom_left = block_center[0] - (block_height / 2), block_center[1] - (block_width/2)
    block = set_up_block (bottom_left, block_height, block_width)
    rotated_block = rotate_points (block, block_center, magnetic_declination)
    
    return {
        'block_json': simplejson.dumps(rotated_block)
        ,'magnetic_declination'                      :  magnetic_declination # degrees
        ,'selected_block_center_y'                   :  selected_block_center_y
        ,'selected_block_center_x'                   :  selected_block_center_x
        ,'block_height_in_m'                         :  block_height_in_m
        ,'block_width_in_m'                          :  block_width_in_m
        ,'num_points'                                :  num_points
        ,'trap_sites'                                :  simplejson.dumps(trap_sites)
        ,'trap_sites_obj'                            :  trap_sites
    
    }
    
