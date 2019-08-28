#!/usr/bin/env python3
import json
import urllib.request
from datetime import datetime, timedelta
from typing import List

CTVRTKON_FEED = 'https://www.ctvrtkon.cz/feed-1.json'


def load_items() -> List[dict]:
    try:
        with urllib.request.urlopen(CTVRTKON_FEED) as f:
            return json.loads(f.read().decode('utf-8'))['items']
    except Exception:
        print(f"Nepodařilo se mi fetchnout feed;( Co tobě?\n{CTVRTKON_FEED}")
        exit(1)


def filter_items_older_than(items: List[dict], allowed_date: datetime) -> List[dict]:
    for i in items:
        if i.get('time') is None:
            continue

        event_time = datetime.strptime(i['time'], '%d.%m.%Y %H:%M')
        if event_time >= allowed_date:
            i['datetime'] = event_time
            yield i


def print_item(item):
    try:
        print('╔═' + '═' * len(item['title']) + '═╗')
        print(f"║ {item['title']} ║")
        print('╚═' + '═' * len(item['title']) + '═╝')
        print()

        print(f"{item['description']}\n")
        print(f"Kdy:  {item['time']}")
        print(f"Kde:  {item['place']}")
        print(f"Link: {item['url']}")
        print(f"FB:   {item['fbEventLink']}")
        print()

    except KeyError:
        print("Nepodařilo se mi rozluštit záznam;(")


if __name__ == '__main__':
    today = datetime.today()
    # today = datetime.today().replace(day=29, hour=19)
    # today = datetime.today().replace(year=2018, month=1)
    # print(today)

    items = load_items()
    items = filter_items_older_than(items, today - timedelta(days=1))
    items = sorted(items, key=lambda k: k['datetime'])

    if items:
        for i in items:
            print_item(i)
    else:
        print("Žádné nadcházející čtvrtkony ;(")
