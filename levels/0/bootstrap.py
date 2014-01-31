import os
import sqlite3

from datetime import date
from uuid import uuid4

#Import override config
try:
    import localsettings as local
except Exception, e:
    local = {}


#NOTE - This step will have different data on 'prod'
def setup_db():
    os.remove('level00.db')

    conn = sqlite3.connect('level00.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE user
                 (user_id integer
                    , admin text
                    , uuid integer
                    , created_date text
                    , first_name text
                    , last_name text
                    , username text
                    , password text
                    , email text)''')

    c.execute('''CREATE TABLE session
                 (session_id text
                  , user_id integer
                  , created_date text)''')

    for stmt in USER_INSERTS:
        c.execute(stmt[0], stmt[1])

    conn.commit()
    conn.close()


today = str(date.today())
USER_INSERTS = getattr(local, 'USER_INSERTS', [
    ("""INSERT INTO user
        (user_id
         , admin
         , uuid
         , created_date
         , first_name
         , last_name
         , username
         , password
         , email)

        VALUES (
            1
            , ?
            , ?
            , ?
            , 'Python'
            , 'Haxor'
            , 'person@pythonmke.org'
            , 'abc123'
            , 'person@pythonmke.org'
        )""", ('false', str(uuid4()), today) ),
    (
        """INSERT INTO user
        (user_id
         , admin
         , uuid
         , created_date
         , first_name
         , last_name
         , username
         , password
         , email)

        VALUES (
            2
            , ?
            , ?
            , ?
            , 'Zaphod'
            , 'Beeblebrox'
            , 'Zaphod.Beeblebrox@gmail.com'
            , 'abc123'
            , 'Zaphod.Beeblebrox@gmail.com'
        )""", ('false', str(uuid4()), today) ),
    (
        """INSERT INTO user
        (user_id
         , admin
         , uuid
         , created_date
         , first_name
         , last_name
         , username
         , password
         , email)

        VALUES (
            3
            , ?
            , ?
            , ?
            , 'Arthur'
            , 'Dent'
            , 'Arthur.Dent@gmail.com'
            , 'abc123'
            , 'Arthur.Dent@gmail.com'
        )""", ('true', str(uuid4()), today) ),
    (
        """INSERT INTO user
        (user_id
         , admin
         , uuid
         , created_date
         , first_name
         , last_name
         , username
         , password
         , email)

        VALUES (
            4
            , ?
            , ?
            , ?
            , 'Ford'
            , 'Prefect'
            , 'Ford.Prefect@gmail.com'
            , 'abc123'
            , 'Ford.Prefect@gmail.com'
        )""", ('false', str(uuid4()), today)
    )
])
