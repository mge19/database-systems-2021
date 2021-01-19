import os
import sys
import psycopg2 as dbapi2

INIT_STATEMENTS = [

    " DROP TABLE USERS CASCADE ",
    " DROP TABLE GROUPS CASCADE",
    " DROP TABLE USER_ALERTS CASCADE",

    " DROP TABLE GROUP_ALERTS CASCADE",

    " DROP TABLE GROUPS_USERS CASCADE"

]

def drop(url):
    with dbapi2.connect(url) as connection:
        i = 0
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            print(i)
            i = i + 1
            cursor.execute(statement)

if __name__ == "__main__":
    url="postgres://htdzjafdlgqcto:e0d12d58a76a23c0d74bcb47834211e2e7d579e5817f7f5830b5f414ac1b18a5@ec2-54-216-155-253.eu-west-1.compute.amazonaws.com:5432/d1m7ithdu0pdc7"
    #url="postgres://postgres:1a2b3c@localhost:5432/postgres"
    print(url)
    if url is None:
        print("Usage: DATABASE_URL=url python dbdrop.py", file=sys.stderr)
        sys.exit(1)
drop(url)

