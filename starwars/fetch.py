
from uuid import uuid4

from dateutil.parser import parse

import petl as etl
import requests


def fetch():
    def download() -> etl.Table:
        next_page = 'https://swapi.dev/api/people/'
        while next_page:
            r = requests.get(next_page)
            data = r.json()
            next_page = data['next']
            yield etl.fromdicts(data['results'])

    fetched = etl.cat(*download())
    characters_with_date = etl.addfield(fetched, 'date', lambda row: parse(row['created']).date())

    def fetch_planets() -> etl.Table:
        next_page = 'https://swapi.dev/api/planets/'
        while next_page:
            r = requests.get(next_page)
            data = r.json()
            next_page = data['next']
            yield etl.fromdicts(data['results'])

    planets = etl.cat(*fetch_planets())
    planets_selected = etl.cut(planets, 'name', 'url')
    planets_renamed = etl.rename(planets_selected, {'name': 'planet_name', 'url': 'planet_url'})
    joined = etl.join(characters_with_date, planets_renamed, lkey='homeworld', rkey='planet_url')
    joined_selected = etl.cut(joined, "name", "height", "mass", "hair_color", "skin_color", "eye_color", "birth_year", "gender", "planet_name", "date")
    joined_selected_renamed = etl.rename(joined_selected, "planet_name", "homeworld")
    file_name = f"{uuid4().hex}.csv"
    joined_selected_renamed.tocsv(file_name)

    return file_name
