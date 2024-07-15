from django.core.management import BaseCommand

from starwars.service import fetch_collection


class Command(BaseCommand):
    help = "Fetch data from the Star Wars API"

    def handle(self, *args, **options):
        fetch_collection()
        self.stdout.write(self.style.SUCCESS("Successfully fetched data"))
