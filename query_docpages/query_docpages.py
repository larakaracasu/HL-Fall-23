# Imports
import aiosql
import os
import psycopg2

# Load and enter environment variables
PGUSER = os.environ['PGUSER']
PGPASSWORD = os.environ['PGPASSWORD']
PGHOST = os.environ['PGHOST']
DATABASE_NAME = "postgres"
DSN = f"dbname='{DATABASE_NAME}' user='{PGUSER}' password='{PGPASSWORD}' host='{PGHOST}'"

# Connect to the database with psycopg2
with psycopg2.connect(DSN) as conn:
    # Load SQL queries
    queries = aiosql.from_path("sql_query_for_docpages.sql", "psycopg2")

    # Execute query - get head() of data
    results = queries.head(conn)

    for result in results:
        print(result)