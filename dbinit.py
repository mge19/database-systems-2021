import os
import sys
import psycopg2 as dbapi2

INIT_STATEMENTS = [
    """ CREATE TABLE IF NOT EXISTS USERS(
            user_id serial PRIMARY KEY,
            first_name varchar(50)  NOT NULL,
            last_name varchar(50)  NOT NULL,
            email varchar(50) UNIQUE NOT NULL,

	    password varchar(250)  NOT NULL
            );""",
                            
    """ CREATE TABLE IF NOT EXISTS GROUPS(
            group_id serial PRIMARY KEY,
            group_name varchar(20) NOT NULL,
            description varchar(100) NOT NULL
            );""",
                    
    """ CREATE TABLE IF NOT EXISTS USER_ALERTS(
            alert_id serial PRIMARY KEY,
            user_id integer,
            alert_time timestamp,
            title varchar(20) NOT NULL,
            message varchar(100) NOT NULL,
            urgency  varchar (6) NOT NULL CHECK (urgency IN ( 'low' , 'medium' , 'high') ), 
            type  varchar (8) NOT NULL CHECK (type IN ( 'task' , 'reminder') ), 
            FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE RESTRICT
            );""",

    """ CREATE TABLE IF NOT EXISTS GROUP_ALERTS(
            alert_id serial PRIMARY KEY,
            group_id integer,
            alert_time timestamp,
            title varchar(20) NOT NULL,
            message varchar(100) NOT NULL,
            urgency  varchar (6) NOT NULL CHECK (urgency IN ( 'low' , 'medium' , 'high') ), 
            type  varchar (8) NOT NULL CHECK (type IN ( 'task' , 'reminder') ), 
            FOREIGN KEY (group_id) REFERENCES GROUPS(group_id) ON DELETE RESTRICT
            );""",
                
    """ CREATE TABLE IF NOT EXISTS GROUPS_USERS(
            user_id integer,
            group_id integer,
            admin varchar(1) NOT NULL CHECK (admin IN ( 'y' , 'n') ), 
            FOREIGN KEY (group_id) REFERENCES GROUPS(group_id) ON DELETE RESTRICT,
            FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE RESTRICT
            );""",
                
]

def initialize(url):
    with dbapi2.connect(url) as connection:
        i = 0
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            print(i)
            i = i + 1
            cursor.execute(statement)

        cursor.close()

if __name__ == "__main__":
    url="postgres://mkstwwsqziogdt:821d366826d60dd49017e47a785b3c588d3bc3d847fd7fc18f6b9fe85abd0d9e@ec2-54-247-158-179.eu-west-1.compute.amazonaws.com:5432/dfl517spu7ensr"
    #url="postgres://postgres:1a2b3c@localhost:5432/postgres"
    print(url)
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
initialize(url)

