from django.contrib.gis import admin
from models import Tree, Plot

admin.site.register(Tree, admin.GeoModelAdmin)
admin.site.register(Plot, admin.GeoModelAdmin)
