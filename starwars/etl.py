from typing import Generator
from uuid import uuid4
from dateutil.parser import parse

import petl as etl
import requests

import httpx
import asyncio


def consume_resource(resource: str) -> Generator[etl.Table, None, None]:
    """Consume a resource from the Star Wars API and return a table."""
    next_page = f"https://swapi.dev/api/{resource}/"
    results = []
    while next_page:
        data = requests.get(next_page).json()
        next_page = data["next"]
        results.extend(data["results"])

    return etl.fromdicts(results)


def fetch() -> str:
    """Fetch Star Wars data and save it to a CSV file."""

    # Download and filter people
    people = consume_resource("people")
    people_with_date = etl.addfield(
        people, "date", lambda row: parse(row["created"]).date()
    )
    people_with_date_and_selected = etl.cut(
        people_with_date,
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "homeworld",
        "date",
    )

    # Download and filter planets
    planets = consume_resource("planets")
    planets_selected = etl.cut(planets, "name", "url")
    planets_selected_renamed = etl.rename(
        planets_selected, {"name": "planet_name", "url": "planet_url"}
    )

    # Join people with planets
    people_with_planets = etl.join(
        people_with_date_and_selected,
        planets_selected_renamed,
        lkey="homeworld",
        rkey="planet_url",
    )

    # Remove the homeworld column and rename the planet_name column to homeworld
    people_with_planets_renamed = etl.cutout(people_with_planets, "homeworld")
    people_with_planets_renamed = etl.rename(
        people_with_planets_renamed, "planet_name", "homeworld"
    )

    # Save the table to a CSV file
    file_name = f"{uuid4().hex}.csv"
    people_with_planets_renamed.tocsv(file_name)

    # Return the file name
    return file_name
