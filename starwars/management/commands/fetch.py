from django.core.management import BaseCommand

from starwars.etl import fetch
from starwars.models import Collection


class Command(BaseCommand):
    help = "Fetch data from the Star Wars API"

    def handle(self, *args, **options):
        file_name = fetch()
        Collection(file=file_name).save()
        self.stdout.write(self.style.SUCCESS("Successfully fetched data"))
