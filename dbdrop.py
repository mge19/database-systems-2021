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
    url="postgres://postgres:1a2b3c@localhost:5432/postgres"
    print(url)
    if url is None:
        print("Usage: DATABASE_URL=url python dbdrop.py", file=sys.stderr)
        sys.exit(1)
drop(url)

