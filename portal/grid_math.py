from math import pi, cos, sin, sqrt, atan, atan2
from portal.grid_math import *

# http://en.wikipedia.org/wiki/World_Geodetic_System
# http://home.online.no/~sigurdhu/Grid_1deg.htm
# according to WGS 84:
# Latitude	minute lat   minute long
# 41deg       1850.90     1402.25	

one_long_degree = 84135.0
one_lat_degree  = 111054.0

def meters_to_degrees_long (x):
    return x / one_long_degree

def meters_to_degrees_lat (y):
    return y / one_lat_degree
    
def degrees_long_to_meters(dlx):
    return dlx * one_long_degree

def degrees_lat_to_meters (dly):
    return dly * one_lat_degree

def to_lat_long (x, y):
    return meters_to_degrees_lat (y), meters_to_degrees_long  (x)
    
def rotate_about_a_point(y, x, center_y, center_x, theta):
    if x == center_x and y == center_y:
        return (y, x)
    if theta == 0:
        return (y, x)
    delta_y = center_y - y
    delta_x = center_x - x
    r = sqrt( delta_y ** 2 + delta_x ** 2 )
    theta_1 = atan2 (delta_x , delta_y) + theta
    return (center_y + cos(theta_1) * r, center_x + sin(theta_1) * r)
