#heatmap.py v1.0 20091004
from PIL import Image,ImageChops
import os
import random
import math
import sys
import colorschemes


class Heatmap:
    """
    Create heatmaps from a list of 2D coordinates.
    
    Based on http://jjguy.com/heatmap/, but adapted to the situation here; no need for KML; instead we're just doing a simple ground overlay in Google Maps.
    """
    def __init__(self):
        self.minXY = ()
        self.maxXY = ()

    def heatmap(self, points, fout, dotsize=50,   opacity=128, size=(1024,1024), scheme="classic"):
    
    
        """
        points  -> an iterable list of tuples, where the contents are the 
                   x,y coordinates to plot. e.g., [(1, 1), (2, 2), (3, 3)]
        fout    -> output file for the PNG
        dotsize -> the size of a single coordinate in the output image in 
                   pixels, default is 150px.  Tweak this parameter to adjust 
                   the resulting heatmap.
        opacity -> the strength of a single coordiniate in the output image.  
                   Tweak this parameter to adjust the resulting heatmap.
        size    -> tuple with the width, height in pixels of the output PNG 
        scheme  -> Name of color scheme to use to color the output image.
                   Use schemes() to get list.  (images are in source distro)
        """
        
        self.dotsize = dotsize
        self.opacity = opacity
        self.size = size
        self.imageFile = fout
 
        self.dotwidth_on_map_lat = None
        self.dotwidth_on_map_lon = None
        self.pixels_per_degree_lat = None
        self.pixels_per_degree_lon = None
 
 
        if scheme not in self.schemes():
            tmp = "Unknown color scheme: %s.  Available schemes: %s"  % (scheme, self.schemes())                           
            raise Exception(tmp)

        #TODO: get this from settings.py
        blackrock_north = 41.43000;
        blackrock_south = 41.37000;
        blackrock_east = -73.98000;
        blackrock_west = -74.07000;
                
        self.minXY, self.maxXY = ((blackrock_south, blackrock_east), (blackrock_north, blackrock_west))
        self.pixels_per_degree_lat =  self.size[0] / abs(blackrock_north - blackrock_south)
        self.pixels_per_degree_lon =  self.size[1] / abs(blackrock_east  - blackrock_west)
        
        self.dotwidth_on_map_lat = self.pixels_per_degree_lat / self.dotsize
        self.dotwidth_on_map_lon = self.pixels_per_degree_lon  / self.dotsize 
        
        dot = self._buildDot(self.dotsize)

        img = Image.new('RGBA', self.size, 'white')
        
        
        for y, x in points: # we're assuming lat /lon coordinates.
            
            tmp = Image.new('RGBA', self.size, 'white')
            tmp.paste( dot, self._translate([y,x]) )
            img = ImageChops.multiply(img, tmp)

        colors = colorschemes.schemes[scheme]        
        self._colorize(img, colors)
        img.save(fout, "PNG")


    def schemes(self):
        """
        Return a list of available color scheme names.
        """
        return colorschemes.schemes.keys() 

    def _buildDot(self, size):
        """ builds a temporary image that is plotted for 
            each point in the dataset"""
        img = Image.new("RGB", (size,size), 'white')
        md = 0.5*math.sqrt( (size/2.0)**2 + (size/2.0)**2 )
        for x in range(size):
            for y in range(size):
                d = math.sqrt( (x - size/2.0)**2 + (y - size/2.0)**2 )
                rgbVal = int(200*d/md + 50)
                rgb = (rgbVal, rgbVal, rgbVal)
                img.putpixel((x,y), rgb)
        return img

    def _colorize(self, img, colors):
        """ use the colorscheme selected to color the 
            image densities  """
        finalVals = {}
        w,h = img.size
        for x in range(w):
            for y in range(h):
                pix = img.getpixel((x,y))
                rgba = list(colors[pix[0]][:3])  #trim off alpha, if it's there.
                if pix[0] <= 254: 
                    alpha = self.opacity
                else:
                    alpha = 0 
                rgba.append(alpha) 
                img.putpixel((x,y), tuple(rgba))


    def _translate(self, point):
        """ translates x,y coordinates from data set into 
        pixel offsets."""
        y = point[0]
        x = point[1]
        #horizontal and vertical ranges for_pixel_centers:
        vrange = float(self.maxXY[0] - self.minXY[0])
        hrange = float(self.maxXY[1] - self.minXY[1])

        #normalize points into range (0 - 1)...
        y = (y - self.minXY[0]) / vrange
        x = (x - self.minXY[1]) / hrange

        #...and the map into our image size...
        
        y = int((1-y)* self.size[0] - self.dotsize / 2)
        x = int((1-x)* self.size[1] - self.dotsize / 2)  
        
        return (x, y)

if __name__ == "__main__":
    pts = []
    for x in range(400):
        pts.append((random.random(), random.random() ))

    #print "Processing %d points..." % len(pts)

    hm = Heatmap()
    hm.heatmap(pts, "classic.png") 
