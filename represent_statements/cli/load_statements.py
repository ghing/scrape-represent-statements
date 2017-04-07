#!/usr/bin/env python

import argparse
from datetime import datetime
import csv
import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from represent_statements.models import Statement


def main():
    parser = argparse.ArgumentParser(
        description="Load statements from CSV into a database.")
    parser.add_argument('--database', default=os.environ.get('DB_URL'),
        help="Database URL.")

    args = parser.parse_args()
    engine = create_engine(args.database)
    Session = sessionmaker(bind=engine)
    session = Session()

    reader = csv.DictReader(sys.stdin)

    for row in reader:
        try:
            date_obj = datetime.strptime(row['date'], '%Y-%m-%d').date()
        except ValueError:
            date_obj = None

        row['date'] = date_obj
        statement = Statement(**row)
        try:
            session.add(statement)
            session.flush()
        except IntegrityError:
            session.rollback()

    session.commit()


if __name__ == "__main__":
    main()
