from django.contrib.gis import admin
from django.contrib.gis.admin import GISModelAdmin
from blackrock.optimization.models import Tree, Plot

admin.site.register(Tree, GISModelAdmin)
admin.site.register(Plot, GISModelAdmin)
