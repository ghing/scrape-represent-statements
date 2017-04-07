#!/usr/bin/env python

import argparse
import csv
from datetime import datetime
import os
import sys
from urllib.parse import urlparse, parse_qs

from lxml.html import document_fromstring
import requests


BASE_URL = 'https://projects.propublica.org/represent/statements/search'
FIELDNAMES = [
    'member',
    'member_url',
    'party',
    'state',
    'district',
    'date',
    'title',
    'url',
]

def fetch_page(q, page, url=BASE_URL):
    payload = {
        'q': q,
        'page': page,
    }
    r = requests.get(url, params=payload)
    doc = document_fromstring(r.text)
    next_page = get_next_page_num(doc)

    return r.text, r.url, next_page


def get_next_page_num(doc):
    a = doc.cssselect('.pagination a.next_page')
    if len(a) == 0:
        return None

    parsed = urlparse(a[0].attrib['href'])
    query = parse_qs(parsed.query)

    return int(query['page'][0])


def parse_statements(html):
    doc = document_fromstring(html)
    rows = doc.cssselect('#statements-table tbody tr')
    return [parse_statement(r) for r in rows]


def parse_statement(row):
    statement = {}
    cols = row.cssselect('td')
    statement['member'] = cols[0].cssselect('a')[0].text_content()
    statement['member_url'] = cols[0].cssselect('a')[0].attrib['href']
    statement['party'] = cols[1].text_content()
    state, district = parse_state_district(cols[2].text_content())
    statement['state'] = state
    statement['district'] = district
    statement['date'] = parse_date(cols[3].text_content())
    statement['title'] = cols[4].cssselect('a')[0].text_content()
    statement['url'] = cols[4].cssselect('a')[0].attrib['href']

    return statement


def parse_state_district(s):
    bits = s.split('-')
    state = bits[0]
    district = None
    if len(bits) > 1:
        district = bits[1]

    return state, district


def parse_date(s):
    if s == "":
        return None

    # HACK
    s = s.replace('Sept.', 'Sep.')
    s = s.replace('July', 'Jul.')
    s = s.replace('June', 'Jun.')
    s = s.replace('May', 'May.')
    s = s.replace('April', 'Apr.')
    s = s.replace('March', 'Mar.')

    try:
        stmt_date = datetime.strptime(s, "%b. %d, %Y")
    except ValueError:
        # No year in date.  Use current year
        stmt_date = datetime.strptime(s, "%b. %d")
        now = datetime.now()
        stmt_date = stmt_date.replace(year=now.year)

    return stmt_date.strftime("%Y-%m-%d")


def main():
    parser = argparse.ArgumentParser(
        description="Scrape statements from ProPublica's Represent app.")
    parser.add_argument('query', type=str, nargs=1,
        help="Query string that will be used to search statements")
    parser.add_argument('--since', default=None,
        help="Don't load any more statements ")

    args = parser.parse_args()

    if args.since is None:
        since = None
    else:
        since = datetime.strptime(args.since, "%Y-%m-%d")

    next_page = 1
    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDNAMES)
    writer.writeheader()

    while next_page is not None:
        html, url, next_page = fetch_page(args.query, next_page)
        statements = parse_statements(html)

        for i, stmt in enumerate(statements):
            stmt_date = datetime.strptime(stmt['date'], "%Y-%m-%d")
            if stmt_date < since:
                next_page = None
                break

            writer.writerow(stmt)


if __name__ == "__main__":
    main()
