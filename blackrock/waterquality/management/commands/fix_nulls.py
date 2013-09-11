from django.core.management.base import BaseCommand
from blackrock.waterquality.models import Row


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        for r in Row.objects.filter(value=None):
            r.value = "0.0"
            r.save()
