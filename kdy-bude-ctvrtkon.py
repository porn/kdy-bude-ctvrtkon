#!/usr/bin/env python3
import json
import urllib.request
from datetime import datetime, timedelta

CTVRTKON_FEED = 'https://ctvrtkon.cz/api/events/feed'


def load_items() -> list[dict]:
    try:
        with urllib.request.urlopen(CTVRTKON_FEED) as f:
            return json.loads(f.read().decode('utf-8'))['data']
    except Exception:
        print(f"Nepodařilo se mi fetchnout feed;( Co tobě?\n{CTVRTKON_FEED}")
        exit(1)


def filter_items_older_than(items: list[dict], allowed_date: datetime) -> list[dict]:
    for i in items:
        if i.get('started_at') is None:
            continue

        event_time = datetime.strptime(i['started_at'], '%Y-%m-%d %H:%M:%S')
        if event_time >= allowed_date:
            i['datetime'] = event_time
            yield i


def print_item(item):
    try:
        print('╔═' + '═' * len(item['name']) + '═╗')
        print(f"║ {item['name']} ║")
        print('╚═' + '═' * len(item['name']) + '═╝')
        print()

        print(f"{item['description']}\n")
        print(f"Kdy:        {item['started_at']}")
        print(f"Kde:        {item['venue']['name']}; {item['venue']['address']} ({item['venue']['website_url']})")
        print(f"Registrace: {item['registration_url']}")
        print(f"FB:         {item['facebook_url']}")
        print()

    except KeyError:
        print("Nepodařilo se mi rozluštit záznam;(")


if __name__ == '__main__':
    today = datetime.today()
    # today = datetime.today().replace(day=29, hour=19)
    # today = datetime.today().replace(year=2023, month=8)
    # print(today)

    items = load_items()
    items = filter_items_older_than(items, today - timedelta(days=1))
    items = sorted(items, key=lambda k: k['datetime'])

    if items:
        for i in items:
            print_item(i)
    else:
        print("Žádné nadcházející čtvrtkony ;(")
