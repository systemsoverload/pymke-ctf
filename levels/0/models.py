from datetime import date
from uuid import uuid4

import sqlite3


def sanitize_input(sql_input):
    '''Prevent user input from messing with SQL queries'''

    try:
        sql_input = (sql_input.lower()
                     .replace('drop', '')
                     .replace('insert', '')
                     .replace('update', ''))
    except:
        #FIXME - add specific exception handling, should be good enough for now
        pass

    return sql_input


class InvalidSession(Exception):
    pass


class AuthenticationError(Exception):
    pass


class User(object):
    '''User model to ease in fetching user from the database
    and returning the data in a nice, neat format'''

    def __init__(self, username=None, user_id=None):
        self.conn = sqlite3.connect('level00.db')

        if username:
            self._get_by_username(username)
        elif user_id:
            self._get_by_user_id(user_id)
        else:
            raise Exception('Unable to construct user without id or username')

        self.conn.close()

    def authenticate(self, password):
        if not password == self.password:
            raise AuthenticationError('Invalid username or password')
        else:
            return True

    def _get_by_username(self, user_name):
        c = self.conn.cursor()
        query = 'SELECT * FROM user WHERE username = ?'
        user_obj = c.execute(query, (user_name.strip(),)).fetchone()
        if user_obj:
            self._setup(user_obj)
        else:
            raise AuthenticationError('Invalid username or password')

    def _get_by_user_id(self, user_id):
        c = self.conn.cursor()

        query = 'SELECT * FROM user WHERE user_id = {0}'.format(sanitize_input(user_id))
        user_obj = c.execute(query).fetchone()
        if user_obj:
            self._setup(user_obj)
        else:
            raise AuthenticationError('Invalid username or password')

    def _setup(self, user_obj):
        self.user_id = user_obj[0]
        self.admin = user_obj[1]
        self.uuid = user_obj[2]
        self.created_date = user_obj[3]
        self.first_name = user_obj[4]
        self.last_name = user_obj[5]
        self.username = user_obj[6]
        self.password = user_obj[7]
        self.email = user_obj[8]


class AnonymousUser(User):
    def __init__(self):
        self.user_id = None
        self.uuid = None
        self.created_date = None
        self.first_name = u"Anonymous"
        self.last_name = u'User'
        self.username = None
        self.password = None
        self.email = None


class Session(object):
    '''Session model to ease in fetching user from the database
    and returning the data in a nice, neat format'''

    def __init__(self, user_id=None, session_id=None):
        self.conn = sqlite3.connect('level00.db')

        if not user_id and not session_id:
            exc = 'Cannot get or create session without user_id or session_id'
            raise Exception(exc)

        if not session_id:
            self.session_id, self.user_id = self._create_session(user_id)
        else:
            self.session_id, self.user_id = self._get_session(session_id)

        self.conn.close()

    def _create_session(self, user_id):
        c = self.conn.cursor()
        today = str(date.today())
        session_id = str(uuid4())
        query = "INSERT INTO session VALUES (?, ?, ?)"
        c.execute(query, (session_id, user_id, today))
        self.conn.commit()

        return self._get_session(session_id)

    def _get_session(self, session_id):
        c = self.conn.cursor()
        query = "SELECT * FROM session WHERE session_id = ?"
        _record = c.execute(query, (session_id,)).fetchone()
        try:
            return _record[0], _record[1]
        except:
            raise InvalidSession('Invalid session {0}'.format(session_id))
