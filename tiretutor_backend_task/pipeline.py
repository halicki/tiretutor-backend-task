from datetime import date

import petl as etl
import requests

def fetch() -> etl.Table:
    next_page = 'https://swapi.dev/api/people/'
    while next_page:
        r = requests.get(next_page)
        data = r.json()
        next_page = data['next']
        yield etl.fromdicts(data['results'])


def extract() -> etl.Table:
    return etl.cat(fetch())


def transform(data: etl.Table) -> etl.Table:
    return etl.addcolumn(data, 'data', lambda row: str(date(row['edited'])))


def main():
    from pprint import pprint
    extracted = extract()
    transformed = transform(extracted)
    pprint(extracted)


if __name__ == "__main__":
    main()