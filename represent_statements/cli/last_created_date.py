#!/usr/bin/env python

import argparse
from datetime import timedelta
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from represent_statements.models import Statement

def main():
    parser = argparse.ArgumentParser(
        description="Get the latest created date of a statement in the database.")
    parser.add_argument('--database', default=os.environ.get('DB_URL'),
        help="Database URL.")
    parser.add_argument('--subtract-days', type=int, default=0,
        help="Subtract this many days from the latest created date")

    args = parser.parse_args()
    engine = create_engine(args.database)
    Session = sessionmaker(bind=engine)
    session = Session()

    last_date = session.query(Statement)\
        .filter(Statement.date != None)\
        .order_by(Statement.created.desc())\
        .first().created

    if args.subtract_days == 0:
        print(last_date.date())

    else:
        print(last_date.date() - timedelta(days=args.subtract_days))


if __name__ == "__main__":
    main()
