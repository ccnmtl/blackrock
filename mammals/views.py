from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext, Context, TemplateDoesNotExist
from django.shortcuts import render_to_response
from django.db import connection 
from django.db.models import get_model, DateField
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, date
from django.contrib.auth.decorators import user_passes_test
from django.utils import simplejson
from django.contrib.gis.geos import  * 
from django.contrib.gis.measure import D # D is a shortcut for Distance 
from django.template.loader import get_template
from mammals.grid_math import *
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, TemplateDoesNotExist
from blackrock.mammals.models import *
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


if 1 == 0:
    @rendered_with('mammals/grid.html')
    def grid(request):
        #butler library:
        #default_lat = 40.80835;
        #default_lon = -73.96455;
        #blackrock
        default_lat = 41.400;
        default_lon = -74.0305;
        
        if (request.method != 'POST'):
            grid_center                             = [default_lat, default_lon]
            height_in_blocks,  width_in_blocks,     = [22, 27]
            block_height_in_m, block_width_in_m     = [250.0, 250.0]
            grid_center_y, grid_center_x = grid_center
            
        else:
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
                grid_json.append (block)
            
        return {
            'grid_json': simplejson.dumps(grid_json)
            ,'grid_center_y'                             :  grid_center_y
            ,'grid_center_x'                             :  grid_center_x
            ,'height_in_blocks'                          :  height_in_blocks
            ,'width_in_blocks'                           :  width_in_blocks
            ,'block_height_in_m'                         :  block_height_in_m
            ,'block_width_in_m'                          :  block_width_in_m    
        }

if 1 == 1:
    @rendered_with('mammals/grid.html')
    def grid(request):
        grid = [gs.info_for_display() for gs in GridSquare.objects.all() if gs.display_this_square]
        
        return {
            'grid_json'                                  :  simplejson.dumps(grid)
            ,'grid_center_y'                             :  41.400
            ,'grid_center_x'                             :  -74.0305
            ,'height_in_blocks'                          :  22
            ,'width_in_blocks'                           :  27
            ,'block_height_in_m'                         :  250.0
            ,'block_width_in_m'                          :  250.0
        }



def pick_transects (center, side_of_square, number_of_transects, number_of_points_per_transect, magnetic_declination):
    result = []    
    for i in range (number_of_transects):
        transect = {}
        transect_heading =  pick_transect_heading()
        transect_length = length_of_transect (transect_heading, side_of_square)
        transect ['heading'] = radians_to_degrees (transect_heading)
        
        tmp = radians_to_degrees (transect_heading ) + magnetic_declination
        if tmp < 0:
            tmp += 360
        transect ['heading_wrt_magnetic_north'] = tmp
        transect ['length'] = transect_length
        transect ['edge'] = walk (center, transect_length, transect_heading)
        points = []
        for j in range (number_of_points_per_transect):
            new_point = {}
            distance = triangular (0, transect_length, transect_length)
            point = walk (center, distance, transect_heading)
            new_point['point']    = point
            new_point['heading']  = radians_to_degrees (transect_heading)
            new_point['distance'] = distance
            points.append (new_point)
        transect['points'] = sorted(points, key= lambda p: (p['distance']))
        result.append (transect)
    sorted_transects = sorted(result, key= lambda t: (t['heading']))
    transect_index, point_index = 0, 0
    for t in sorted_transects:
        transect_index += 1
        t['transect_id'] = transect_index
        for p in t['points']:
            point_index += 1
            p['point_id'] = point_index
            p['transect_id'] = transect_index
    return sorted_transects



    
def pick_trap_location (center, max_distance_from_center_y, max_distance_from_center_x, rotate_by):
        
    y_distance = uniform(0, abs(max_distance_from_center_y))
    x_distance = uniform(0, abs(max_distance_from_center_x))
    y_direction = choice(['north', 'south'])
    x_direction = choice(['east',  'west'])
    #The die has been cast.    
    
    #figure out distances:
    if y_direction == 'south':
        dy = - y_distance
    else:
        dy =   y_distance
    
    if x_direction == 'west':
        dx = - x_distance
    else:    
        dx =   x_distance
    
    #figure out where the point is:
    center_meters = to_meters_point (center)
    tmp = to_lat_long(center_meters[0] - dy, center_meters[1] - dx)

    #describe the point:
    result = {}    
    result ['point']           = tmp
    
    result ['distance_y']      = y_distance
    result ['distance_x']      = x_distance
    result ['actual_distance'] = hypotenuse (y_distance, x_distance)
    
    #directions returned are with respect to compass north
    result ['direction_y']     = y_direction
    result ['direction_x']     = x_direction
    result ['heading']         = radians_to_degrees(atan2(dx, dy))
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
        num_transects                           = 2
        points_per_transect                     = 2 
        height_in_blocks,  width_in_blocks,     = [22, 27]
        radius_of_circles                       = 0.0 # degrees
        magnetic_declination                    = -13.0 # degrees
        block_center                             = [default_lat, default_lon]
        block_height_in_m, block_width_in_m     = [250.0, 250.0]
        grid_center_y, grid_center_x = grid_center
        selected_block_center_y, selected_block_center_x = block_center
    else:
        num_transects        =                  get_int  ( request, 'num_transects',            2 )
        points_per_transect  =                  get_int  ( request, 'points_per_transect',      2 )
        radius_of_circles    =                  get_float( request, 'radius_of_circles',        30.0 )
        magnetic_declination =                  get_float( request, 'magnetic_declination',     -13.0 )
        block_height_in_m =                     get_float( request, 'block_height_in_m',        250.0)
        block_width_in_m  =                     get_float( request, 'block_width_in_m',         250.0)
        selected_block_center_y =               get_float( request, 'selected_block_center_y',  default_lat)
        selected_block_center_x =               get_float( request, 'selected_block_center_x',  default_lon)
        grid_center_y           =               get_float( request, 'grid_center_y',            default_lat)
        grid_center_x           =               get_float( request, 'grid_center_x',            default_lon)
        height_in_blocks =                      get_int( request,   'height_in_blocks',         21)
        width_in_blocks   =                     get_int( request,   'width_in_blocks',          27)
        block_center = selected_block_center_y, selected_block_center_x
    block_height, block_width    = to_lat_long (block_height_in_m,  block_width_in_m )
    
    transects = []
    transects = pick_transects (block_center, block_width_in_m, num_transects, points_per_transect, magnetic_declination)

    bottom_left = block_center[0] - (block_height / 2), block_center[1] - (block_width/2)
    block = set_up_block (bottom_left, block_height, block_width)
    
    test_points = []    
    
    #######
    if  1 == 0:
        test_points = []
        center_meters = to_meters  (block_center[0], block_center[1])
        side_of_square = block_height_in_m
        for i in range (360):
            radians = degrees_to_radians (float(i))
            l = length_of_transect (radians, side_of_square)
            new_point = [center_meters[0] + sin (radians) * l, center_meters[1] + cos (radians) * l]
            test_points.append ( to_lat_long(new_point[0], new_point[1] ))
    ############
        
    return {
        'block_json': simplejson.dumps(block)
        ,'radius_of_circles'                         :  radius_of_circles # meters
        ,'magnetic_declination'                      :  magnetic_declination # degrees
        ,'points_per_transect'                       :  points_per_transect # meters
        ,'num_transects'                             :  num_transects # degrees
        ,'selected_block_center_y'                   :  selected_block_center_y
        ,'selected_block_center_x'                   :  selected_block_center_x
        ,'block_height_in_m'                         :  block_height_in_m
        ,'block_width_in_m'                          :  block_width_in_m
        ,'grid_center_y'                             :  grid_center_y
        ,'grid_center_x'                             :  grid_center_x
        ,'height_in_blocks'                          :  height_in_blocks
        ,'width_in_blocks'                           :  width_in_blocks
        ,'transects_json'                            :  simplejson.dumps(transects)
        ,'transects'                                 :  transects
    
    }
    
