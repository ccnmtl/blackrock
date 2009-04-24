from django.contrib.gis import admin
from models import Tree

admin.site.register(Tree, admin.GeoModelAdmin)
