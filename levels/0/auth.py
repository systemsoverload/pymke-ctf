from functools import wraps

from flask import g, redirect, url_for, request


def login_required(func):
    '''Helper to enforce user authentcation on wrapped views'''

    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            g.user
        except:
            return redirect(url_for('login', next=request.url))

        return func(*args, **kwargs)
    return decorated_function
