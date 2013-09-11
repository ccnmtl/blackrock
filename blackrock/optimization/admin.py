from django.contrib.gis import admin
from blackrock.optimization.models import Tree, Plot

admin.site.register(Tree, admin.GeoModelAdmin)
admin.site.register(Plot, admin.GeoModelAdmin)
