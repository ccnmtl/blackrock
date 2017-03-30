# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def fix_image_path(path):
    """Fix image path for this habitat.

    This function takes a path. If it looks like this:
      '/mammals/media/images/habitat_map/habitat_960.png'

    it returns something like this:
      '/images/mammals/habitat_map/habitat_960.png'
    """
    if path.startswith('/mammals/media/images/'):
        return path.replace('/mammals/media/images/', '/images/mammals/', 1)

    return path


def fix_image_paths(apps, schema_editor):
    Habitat = apps.get_model('mammals', 'Habitat')
    for habitat in Habitat.objects.all():
        habitat.image_path_for_legend = fix_image_path(
            habitat.image_path_for_legend)
        habitat.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mammals', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fix_image_paths),
    ]
