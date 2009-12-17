from blackrock.paleoecology.models import PollenSample, PollenType
from django.contrib import admin

class PollenSampleAdmin(admin.ModelAdmin):
  list_display = ('depth', 'pollen', 'percentage', 'count')
  list_filter = ('depth', 'pollen')
  ordering = ('depth', 'pollen')
  #search_fields = ('depth', 'pollen')

class PollenTypeAdmin(admin.ModelAdmin):
  ordering = ('name',)

admin.site.register(PollenSample, PollenSampleAdmin)
admin.site.register(PollenType, PollenTypeAdmin)
