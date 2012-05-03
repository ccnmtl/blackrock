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

class GradeLevelAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields = ('label',)

admin.site.register(GradeLevel, GradeLevelAdmin)

class BaitAdmin (admin.ModelAdmin):
    list_display = (  'bait_name',)
    fields = ('bait_name',)

admin.site.register(Bait, BaitAdmin)

class SpeciesAdmin (admin.ModelAdmin):
    list_display = (  'latin_name','common_name',)
    fields =  (  'latin_name','common_name', 'about_this_species',)
admin.site.register(Species, SpeciesAdmin)

class AnimalAdmin (admin.ModelAdmin):
    list_display = (  'species',)
    fields =  (  'species','tag_info', 'description',)
admin.site.register(Animal, AnimalAdmin)

class TrapAdmin (admin.ModelAdmin):
    list_display = (  'trap_string',)
    fields =  (  'trap_string',)
admin.site.register(Trap, TrapAdmin)


class HabitatAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields       =(  'label', 'blurb')
admin.site.register(Habitat, HabitatAdmin)


class ExpeditionAdmin (admin.ModelAdmin):
    list_display = (  '__unicode__', 'number_of_students', 'grade_level', 'grid_square',)
    fields       = (
        #'start_date_of_expedition',
        #'end_date_of_expedition',
        #'created_on',
        'number_of_students',
        'grade_level',
        'grid_square',
        
        'school_contact_1_phone',
        'school_contact_1_email',
        'school_contact_2_phone',
        'school_contact_2_email',
        
        'notes_about_this_expedition', 
        'created_by',
    )
admin.site.register(Expedition, ExpeditionAdmin)


    
class TrapLocationAdmin (admin.ModelAdmin):
    list_display = (  'expedition', 'geo_point','trap_used', 'bait', 'habitat',)
    fields       = ( 'expedition', 'geo_point', 'trap_used', 'bait', 'habitat',  'notes_about_location', 'animal', 'notes_about_outcome' )
    
admin.site.register(TrapLocation, TrapLocationAdmin)


