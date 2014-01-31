import bootstrap
import re

from flask import (
    Flask, render_template, g, request, redirect, url_for, make_response)

from auth import login_required
from models import (
    User, Session, InvalidSession, AuthenticationError)

#Import override config
try:
    import localsettings as local
except Exception, e:
    local = {}


bootstrap.setup_db()
app = Flask(__name__)
app.secret_key = '9<0FKH2W7"678+b'
SECRET_CODE = getattr(local, 'SECRET_CODE', '189257897-89789789709-')


@app.before_request
def before_request():
    '''Before all requests, look up and validate users session'''

    session_id = request.cookies.get('session')
    if session_id:
        try:
            session_user_id = Session(session_id=session_id).user_id
            g.user = User(user_id=session_user_id)
        except InvalidSession:
            if request.path != '/login':
                return redirect(url_for('login', next=request.url))

    elif not session_id and request.path != '/login':
        return redirect(url_for('login', next=request.url))
    else:
        return


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        errors = []
        username = request.form.get('username')
        password = request.form.get('password')

        if not username and password:
            errors.append('Missing required username or password field')

        try:
            user = User(username=username)
            user.authenticate(password=password)
        except AuthenticationError, e:
            errors.append(e)

        if not errors:
            next = request.form.get('next', '/')
            response = make_response(redirect(next))

            session = Session(user_id=user.user_id)
            response.set_cookie('session', value=session.session_id)
            return response
        else:
            return render_template("login.html", errors=errors)
    else:
        next = request.values.get('next', '')

        return render_template("login.html", next=next)


@app.route('/')
def index():
    return render_template('level00.html', user=g.user, secret_code=SECRET_CODE)


@app.route('/profile/<user_id>')
@login_required
def profile(user_id):
    '''Display user profile information about currently logged in user'''

    #Prevent users from accessing other peoples profiles
    if int(re.sub("[^0-9]", "", user_id)) != g.user.user_id:
        return "Unauthorized Access!!!!"

    user = User(user_id=user_id)
    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
