from blackrock.mammals.models import *
from django.contrib import admin

class GridPointAdmin (admin.ModelAdmin):
    list_display = ( 'geo_point',)
    fields = ('geo_point',)
admin.site.register(GridPoint, GridPointAdmin)

class GridSquareAdmin (admin.ModelAdmin):
    list_filter = ('display_this_square', 'row', 'column',)
    list_display = (  '__unicode__', 'display_this_square','center', 'row', 'column', 'access_difficulty', 'label_2',)
    fields = (  'row', 'column', 'display_this_square', 'access_difficulty', 'center', 'NW_corner', 'NE_corner', 'SW_corner', 'SE_corner',   'label_2', )
admin.site.register(GridSquare, GridSquareAdmin)
