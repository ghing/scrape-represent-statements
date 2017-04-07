ProPublica Represent Statement Scraper
======================================

Scrape congressional press releases and other statements from [ProPublica's Represent News Application](https://projects.propublica.org/represent/statements).

Assumptions
-----------

* Python 3.2+

Scrape the statements
---------------------

To scrape all statements matching the search `Town Hall`:

    scrape_statements "Town Hall" > statements__town_hall.csv

To scrape all statements matching the search `Town Hall` since 2017-02-09:

    scrape_statements --since 2017-02-09 "Town Hall"

All together now
----------------

    scrape_statements --since $(last_created_date --subtract-days=1) "Town Hall" | load_statements

We use `last_created_date --subtract-days=1` to get the `--since` argument to `scrape_statements` so we only download statements that are possibly not in the database.  We specify `--subtract-days=1` in order to accomodate time zone differences since we store dates in UTC in the database.

Configuration
-------------

Configuration happens through environment variables.  It might be helpful to put the definitions in a `.env` file in your local development environment.  Then, when running commands, you can do things like:

    env $(cat .env | xargs) scrape_statements "Town Hall" > statements__town_hall.csv

or

    set -a
    . .env
    set +a
    scrape_statements "Town Hall" > statements__town_hall.csv

Database migrations
-------------------

To run database migrations:

    DB_URL=postgresql:///represent_statements alembic upgrade head


