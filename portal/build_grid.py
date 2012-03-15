from portal.grid_math import *
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, TemplateDoesNotExist

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

def get_float (request, name, default):
    number =request.POST.get(name, default)
    return float (number)


def get_int (request, name, default):
    number =request.POST.get(name, default)
    return int (number)


#def get_two_numbers_number (request, names, default_tuples):
#    number =request.POST.get('magnetic_declination', default)
#    return float (number)

@rendered_with('portal/grid.html')
def grid(request):

    #butler library:
    #default_lat = 40.80835;
    #default_lon = -73.96455;
    
    
    #blackrock
    default_lat = 41.397;
    default_lon = -74.021;

    
    if (request.method != 'POST'):
        magnetic_declination                    = -13.0 # degrees
        grid_center                             = [default_lat, default_lon]
        height_in_blocks,  width_in_blocks,     = [2, 3]
        block_height_in_m, block_width_in_m     = [250.0, 250.0]
        grid_center_y, grid_center_x = grid_center
        
    else:
        magnetic_declination =                  get_float( request, 'magnetic_declination',     -13.0)
        height_in_blocks =                      get_int( request,   'height_in_blocks',         2)
        width_in_blocks   =                     get_int( request,   'width_in_blocks',          3)
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

    #tp_1 = grid_center
    #tp_2 = ( grid_center[0], grid_center[1] + meters_to_degrees_long(2000.0))
    #tp_3 = rotate_about_a_point (tp_2, tp_1, 90.0)
    
    
    
    return {
        'grid_json': simplejson.dumps(grid_json)
        #,'test_points': simplejson.dumps((tp_1, tp_2, tp_3))
        ,'magnetic_declination'                      :  magnetic_declination # degrees
        ,'grid_center_y'                             :  grid_center_y
        ,'grid_center_x'                             :  grid_center_x
        ,'height_in_blocks'                          :  height_in_blocks
        ,'width_in_blocks'                           :  width_in_blocks
        ,'block_height_in_m'                         :  block_height_in_m
        ,'block_width_in_m'                          :  block_width_in_m
    
    }
    
@rendered_with('portal/grid_block.html')
def grid_block(request):

    #butler library:
    #default_lat = 40.80835;
    #default_lon = -73.96455;
    
    #blackrock
    default_lat = 41.397;
    default_lon = -74.021;

    
    if (request.method != 'POST'):
        magnetic_declination                    = -13.0 # degrees
        grid_center                             = [default_lat, default_lon]
        block_height_in_m, block_width_in_m     = [250.0, 250.0]
        grid_center_y, grid_center_x = grid_center
        
    else:
        magnetic_declination =                  get_float( request, 'magnetic_declination',     -13.0)
        block_height_in_m =                     get_float( request, 'block_height_in_m',        250.0)
        block_width_in_m  =                     get_float( request, 'block_width_in_m',         250.0)
        grid_center_y          =                get_float( request, 'grid_center_y',            default_lat)
        grid_center_x           =               get_float( request, 'grid_center_x',            default_lon)
        grid_center = grid_center_y, grid_center_x
    
    grid_height_in_m = block_height_in_m 
    grid_width_in_m  = block_width_in_m  
    
    block_height, block_width  = to_lat_long (block_height_in_m,  block_width_in_m )
    grid_height,  grid_width   = to_lat_long (grid_height_in_m,   grid_width_in_m  )
    
    grid_bottom,  grid_left  = grid_center[0] - (grid_height / 2), grid_center[1] - (grid_width/2)
    bottom_left = grid_bottom , grid_left
    block = set_up_block (bottom_left, block_height, block_width)
    rotated_block = rotate_points (block, grid_center, magnetic_declination)

    #tp_1 = grid_center
    #tp_2 = ( grid_center[0], grid_center[1] + meters_to_degrees_long(2000.0))
    #tp_3 = rotate_about_a_point (tp_2, tp_1, 90.0)
    
    
    
    return {
        'grid_json': simplejson.dumps(rotated_block)
        #,'test_points': simplejson.dumps((tp_1, tp_2, tp_3))
        ,'magnetic_declination'                      :  magnetic_declination # degrees
        ,'grid_center_y'                             :  grid_center_y
        ,'grid_center_x'                             :  grid_center_x
        ,'block_height_in_m'                         :  block_height_in_m
        ,'block_width_in_m'                          :  block_width_in_m
    
    }
    
