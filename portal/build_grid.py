from math import pi, cos, sin, sqrt, atan, atan2
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


@rendered_with('portal/grid_demo.html')
def grid_demo(request):

    #  (brf_y_deg, brf_x_deg) =    (41.392, -74.015)
    (brf_y_deg, brf_x_deg)  = (41.397,-74.021)
    width_in_blocks , height_in_blocks,  = (1, 1)
    #width_in_blocks , height_in_blocks,  = (30, 21)
    #block_height_in_m, block_width_in_m   = (250.0, 500.0)


    block_height_in_m, block_width_in_m   = (1000.0, 2000.0)

    
    #magnetic_declination = -13.0
    magnetic_declination = 13.0
    
    theta = magnetic_declination * pi / 180.0 #same thing in radians
    
    
    (grid_width_in_m, grid_height_in_m )  = (block_width_in_m * width_in_blocks, block_height_in_m * height_in_blocks)
    
    #convert to lat/long coordinates:
    
    (block_width_in_deg, block_height_in_deg) = to_lat_long (block_width_in_m, block_height_in_m) 
    (grid_height_in_deg, grid_width_in_deg ) =  to_lat_long (grid_height_in_m,  grid_width_in_m )
    
    #now switching grid_left_in_deg and grid_top_in_deg
    
    (grid_top_in_deg, grid_left_in_deg) = (brf_y_deg - (grid_height_in_deg / 2), brf_x_deg - (grid_width_in_deg/2))
    
    grid_json = []
    
    for i in range (0, height_in_blocks):
        new_row = []
        for j in range (0, width_in_blocks):
            
            top_left_of_block_y = grid_top_in_deg   + i * block_width_in_deg
            top_left_of_block_x = grid_left_in_deg  + j * block_height_in_deg
            
            top_left_of_block = (top_left_of_block_y, top_left_of_block_x)
        
            #move all points to the top left of the BLOCK.            
            (block_1_x, block_1_y) = top_left_of_block
            (block_2_x, block_2_y) = top_left_of_block
            (block_3_x, block_3_y) = top_left_of_block
            (block_4_x, block_4_y) = top_left_of_block
            (block_5_x, block_5_y) = top_left_of_block
            
            #NOW move the x for 2 and 3 over by one block width:
            block_2_x += block_width_in_deg
            block_3_x += block_width_in_deg
            
            #NOW move the y for 3 and 4 over by one block height:
            block_3_y += block_height_in_deg
            block_4_y += block_height_in_deg
            
            #And the center marker gets half-a-width added to both x and y:
            block_5_x += (block_width_in_deg /  2)
            block_5_y += (block_height_in_deg / 2)
            
            
            #rotate everything and add the block on to the row.
            new_block = [
                rotate_about_a_point(block_1_x, block_1_y, brf_y_deg, brf_x_deg, theta)  # top left
               ,rotate_about_a_point(block_2_x, block_2_y, brf_y_deg, brf_x_deg, theta)  # top right
               ,rotate_about_a_point(block_3_x, block_3_y, brf_y_deg, brf_x_deg, theta)  # bottom right
               ,rotate_about_a_point(block_4_x, block_4_y, brf_y_deg, brf_x_deg, theta)  # bottom left
               
               ,rotate_about_a_point(block_5_x, block_5_y, brf_y_deg, brf_x_deg, theta)  # center
            ] 
            new_row.append ( new_block )
        
        #add the row of blocks to the grid:
        grid_json.append (new_row)
            

    return {'grid_json': simplejson.dumps(grid_json)}
    
