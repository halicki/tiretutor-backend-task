from starwars.etl import fetch
from starwars.models import Collection


def fetch_collection():
    file_name = fetch()
    Collection(file=file_name).save()
