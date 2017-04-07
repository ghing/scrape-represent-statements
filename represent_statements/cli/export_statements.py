#!/usr/bin/env python

import argparse
import csv
from datetime import datetime
import os
import sys

from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker

from represent_statements.models import Statement


def parse_state_district(district):
    bits = district.split('-')
    state = bits[0]
    district = None
    if len(bits) > 1:
        district = bits[1]

    return state, district


def main():
    parser = argparse.ArgumentParser(
        description="Load statements from CSV into a database.")
    parser.add_argument('--database', default=os.environ.get('DB_URL'),
        help="Database URL.")
    parser.add_argument('--district', help="District.", action='append')
    parser.add_argument('--since', default=None,
        help="Don't load any more statements ")

    args = parser.parse_args()
    if args.since is None:
        since = None
    else:
        since = datetime.strptime(args.since, "%Y-%m-%d").date()

    engine = create_engine(args.database)
    Session = sessionmaker(bind=engine)
    session = Session()

    fieldnames = [
        'member',
        'member_url',
        'party',
        'state',
        'district',
        'date',
        'title',
        'url',
    ]

    queries = []
    for state_district in args.district:
        state, district = parse_state_district(state_district)
        queries.append(
            and_(Statement.state == state, Statement.district == district))

    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    query = session.query(Statement).filter(or_(*queries))
    if since is not None:
        query = query.filter(Statement.date >= since)

    for stmt in query:
        stmt_dict = {f: getattr(stmt, f) for f in fieldnames}
        writer.writerow(stmt_dict)


if __name__ == "__main__":
    main()
