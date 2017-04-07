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

    scrape_statements --since `last_statement_date` "Town Hall" | load_statements

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


