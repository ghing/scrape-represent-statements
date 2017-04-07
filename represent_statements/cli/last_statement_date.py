#!/usr/bin/env python

import argparse
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from represent_statements.models import Statement


def main():
    parser = argparse.ArgumentParser(
        description="Get the date of the latest statement in the database.")
    parser.add_argument('--database', default=os.environ.get('DB_URL'),
        help="Database URL.")

    args = parser.parse_args()
    engine = create_engine(args.database)
    Session = sessionmaker(bind=engine)
    session = Session()

    last_date = session.query(Statement)\
        .filter(Statement.date != None)\
        .order_by(Statement.date.desc())\
        .first().date
    print(last_date)


if __name__ == "__main__":
    main()
