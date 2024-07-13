import pathlib

import petl
from mockito import mock

import responses


@responses.activate
def test_fetch(when):
    from starwars.etl import fetch

    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/",
        json={
            "next": None,
            "results": [
                {
                    "name": "Luke Skywalker",
                    "height": "172",
                    "mass": "77",
                    "hair_color": "blond",
                    "homeworld": "https://swapi.dev/api/planets/1/",
                    "skin_color": "fair",
                    "eye_color": "blue",
                    "birth_year": "19BBY",
                    "gender": "yes",
                    "created": "2014-12-09T13:50:51.644000Z",
                },
            ],
        },
    )
    responses.add(
        responses.GET,
        "https://swapi.dev/api/planets/",
        json={
            "next": None,
            "results": [
                {"name": "Tatooine", "url": "https://swapi.dev/api/planets/1/"},
            ],
        },
    )
    # mock the uuid4 function
    when("starwars.etl").uuid4().thenReturn(mock({"hex": "1234"}))

    file_name = fetch()

    table = petl.fromcsv(file_name)
    assert table[0] == (
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "date",
        "homeworld",
    )
    assert table[1] == (
        "Luke Skywalker",
        "172",
        "77",
        "blond",
        "fair",
        "blue",
        "19BBY",
        "yes",
        "2014-12-09",
        "Tatooine",
    )

    pathlib.Path(file_name).unlink()
