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


class SchoolAdmin (admin.ModelAdmin):
    list_display = (  'name',)
    fields = ('name',)
admin.site.register(School, SchoolAdmin)

class SpeciesAdmin (admin.ModelAdmin):
    list_display = (  'latin_name','common_name',)
    fields =  (  'latin_name','common_name', 'about_this_species',)
admin.site.register(Species, SpeciesAdmin)

class AnimalAdmin (admin.ModelAdmin):
    list_display = (  'species',) 
    fields =  (  'species','description', 'sex', 'age', 'scale_used', 'tag_number', 'health', 'weight_in_grams', 'recaptured', 'scat_sample_collected', 'blood_sample_collected', 'hair_sample_collected', 'skin_sample_collected',  )
admin.site.register(Animal, AnimalAdmin)

class TrapAdmin (admin.ModelAdmin):
    list_display = (  'trap_string',)
    fields =  (  'trap_string',)
admin.site.register(Trap, TrapAdmin)


class HabitatAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields       =(  'label', 'blurb', 'image_path_for_legend')
admin.site.register(Habitat, HabitatAdmin)


class ExpeditionMoonPhaseAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields       =(  'label',)
admin.site.register(ExpeditionMoonPhase, ExpeditionMoonPhaseAdmin)


class ExpeditionOvernightTemperatureAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields       =(  'label',)
admin.site.register(ExpeditionOvernightTemperature, ExpeditionOvernightTemperatureAdmin)


class ExpeditionOvernightPrecipitationAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields       =(  'label',)
admin.site.register(ExpeditionOvernightPrecipitation, ExpeditionOvernightPrecipitationAdmin)


class ExpeditionOvernightPrecipitationTypeAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields       =(  'label',)
admin.site.register(ExpeditionOvernightPrecipitationType, ExpeditionOvernightPrecipitationTypeAdmin)


class ExpeditionCloudCoverAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields       =(  'label',)
admin.site.register(ExpeditionCloudCover, ExpeditionCloudCoverAdmin)

class IlluminationAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields       =(  'label',)
admin.site.register(Illumination, IlluminationAdmin)


class TrapTypeAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields       =(  'label',)
admin.site.register(TrapType, TrapTypeAdmin)

class AnimalScaleUsedAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields       =(  'label',)
admin.site.register(AnimalScaleUsed, AnimalScaleUsedAdmin)

class AnimalSexAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields       =(  'label',)
admin.site.register(AnimalSex, AnimalSexAdmin)

class AnimalAgeAdmin (admin.ModelAdmin):
    list_display = (  'label',)
    fields       =(  'label',)
admin.site.register(AnimalAge, AnimalAgeAdmin)




class ExpeditionAdmin (admin.ModelAdmin):
    list_display = (  '__unicode__', 'number_of_students', 'grade_level', 'grid_square', 'school',)
    fields       = (
        #'start_date_of_expedition',
        #'end_date_of_expedition',
        #'created_on',
        'number_of_students',
        'grade_level',
        'school',
        'grid_square',
        
        #'school_contact_1_phone',
        #'school_contact_1_email',
        #'school_contact_2_phone',
        #'school_contact_2_email',
        
        'notes_about_this_expedition', 
        'created_by',
        
        'understory',
        'field_notes',
        'cloud_cover',
        'overnight_temperature',
        'overnight_precipitation',
        'overnight_precipitation_type',
        'moon_phase',
        'illumination',
        
        
    )
admin.site.register(Expedition, ExpeditionAdmin)


    
class TrapLocationAdmin (admin.ModelAdmin):
    list_display = (  'expedition', 'suggested_point','actual_point','trap_type', 'bait', 'habitat',)
    fields       = ( 'expedition', 'suggested_point','actual_point', 'trap_type', 'bait', 'habitat',  'notes_about_location', 'animal', 'notes_about_outcome' )
    
admin.site.register(TrapLocation, TrapLocationAdmin)


