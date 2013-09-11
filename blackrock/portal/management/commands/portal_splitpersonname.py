from django.core.management.base import BaseCommand
from blackrock.portal.models import Person


class Command(BaseCommand):

    def handle(self, *app_labels, **options):
        people = Person.objects.all()

        for person in people:
            parts = person.full_name.rpartition(' ')
            person.first_name = parts[0]
            person.last_name = parts[2]
            person.save()
