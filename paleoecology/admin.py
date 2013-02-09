from blackrock.paleoecology.models import PollenSample, PollenType, CoreSample
from django.contrib import admin


class CoreSampleAdmin(admin.ModelAdmin):
    list_display = ('depth',)
    list_filter = ('depth',)
    ordering = ('depth',)


class PollenSampleAdmin(admin.ModelAdmin):
    list_display = ('core_sample', 'pollen', 'count', 'percentage')
    list_filter = ('core_sample', 'pollen')


class PollenTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    ordering = ('name',)

admin.site.register(CoreSample, CoreSampleAdmin)
admin.site.register(PollenSample, PollenSampleAdmin)
admin.site.register(PollenType, PollenTypeAdmin)
