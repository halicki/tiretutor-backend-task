from uuid import uuid4
from dateutil.parser import parse

import petl as etl
import requests


def fetch():
    def download(resource: str) -> etl.Table:
        next_page = f"https://swapi.dev/api/{resource}/"
        while next_page:
            r = requests.get(next_page)
            data = r.json()
            next_page = data["next"]
            yield etl.fromdicts(data["results"])

    people = etl.cat(*download("people"))
    people_selected = etl.cut(
        people,
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "homeworld",
    )

    people_date = etl.addfield(people, "date", lambda row: parse(row["created"]).date())

    planets = etl.cat(*download("planets"))
    planets_selected = etl.cut(planets, "name", "url")
    planets_selected_renamed = etl.rename(
        planets_selected, {"name": "planet_name", "url": "planet_url"}
    )
    people_planets = etl.join(
        people_date, planets_selected_renamed, lkey="homeworld", rkey="planet_url"
    )
    joined_selected = etl.cut(
        people_planets,
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "planet_name",
        "date",
    )
    joined_selected_renamed = etl.rename(joined_selected, "planet_name", "homeworld")
    file_name = f"{uuid4().hex}.csv"
    joined_selected_renamed.tocsv(file_name)

    return file_name
