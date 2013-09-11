from django.core.management.base import BaseCommand
from blackrock.portal.models import Location
from django.contrib.gis.measure import D  # D is a shortcut for Distance


class Command(BaseCommand):

    def handle(self, *app_labels, **options):

        loc = Location.objects.get(name="Tamarack Pond")

        qs = Location.objects.filter(
            latlong__distance_lte=(loc.latlong, D(mi=.1)))

        for loc in qs:
            all_related = loc._meta.get_all_related_objects()
            for obj in all_related:
                for instance in getattr(loc, obj.get_accessor_name()).all():
                    print "%s, %s, [%s, %s]" % (instance._meta.object_name,
                                                instance.name,
                                                instance.location.latlong.x,
                                                instance.location.latlong.y)
