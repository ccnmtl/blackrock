from blackrock.portal.models import Audience, DigitalFormat, Facet, \
    Institution, LocationSubtype, LocationType, PersonType, PublicationType, \
    RegionType, RightsType, Tag, Url, DigitalObject, Location, Station, \
    Region, Person, DataSet, Publication, ResearchProject, LearningActivity, \
    ForestStory, PhotoGalleryItem
from django.contrib import admin


class GenericAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ["name"]

admin.site.register(Audience, GenericAdmin)
admin.site.register(DigitalFormat, GenericAdmin)


class FacetAdmin(admin.ModelAdmin):
    search_fields = ['name', 'display_name', 'facet']
    list_display = ('facet', 'name', 'display_name')
    ordering = ["facet", "name"]
admin.site.register(Facet, FacetAdmin)

admin.site.register(Institution, GenericAdmin)
admin.site.register(LocationType, GenericAdmin)
admin.site.register(LocationSubtype, GenericAdmin)
admin.site.register(PersonType, GenericAdmin)
admin.site.register(PublicationType, GenericAdmin)
admin.site.register(RegionType, GenericAdmin)
admin.site.register(RightsType, GenericAdmin)
admin.site.register(Tag, GenericAdmin)
admin.site.register(Url, GenericAdmin)


class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'latitude', 'longitude')
    ordering = ["name"]
    readonly_fields = ['latlong']

admin.site.register(Location, LocationAdmin)


class StationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ["name"]
admin.site.register(Station, StationAdmin)


class PersonAdmin(admin.ModelAdmin):
    search_fields = ['last_name']
    ordering = ["last_name", "first_name"]
    list_display = ('last_name', 'first_name', 'full_name')
admin.site.register(Person, PersonAdmin)


class DataSetAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ["name"]
admin.site.register(DataSet, DataSetAdmin)


class DigitalObjectAdmin(admin.ModelAdmin):
    search_fields = ['name', 'digital_format']
    list_display = ('name', 'digital_format')
    ordering = ["name"]
admin.site.register(DigitalObject, DigitalObjectAdmin)


class PublicationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ["name"]
admin.site.register(Publication, PublicationAdmin)


class RegionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ["name"]
admin.site.register(Region, RegionAdmin)


class ResearchProjectAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ["name"]
admin.site.register(ResearchProject, ResearchProjectAdmin)


class LearningActivityAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ["name"]
admin.site.register(LearningActivity, LearningActivityAdmin)


class ForestStoryAdmin(admin.ModelAdmin):
    search_fields = ['display_name', 'name', 'description']
    ordering = ["display_name"]
    list_display = ('display_name',)

admin.site.register(ForestStory, ForestStoryAdmin)
admin.site.register(PhotoGalleryItem)


import django_databrowse

django_databrowse.site.register(Station)
django_databrowse.site.register(Person)
django_databrowse.site.register(DataSet)
django_databrowse.site.register(ResearchProject)
django_databrowse.site.register(LearningActivity)
django_databrowse.site.register(ForestStory)

django_databrowse.site.register(Facet)
django_databrowse.site.register(Tag)
