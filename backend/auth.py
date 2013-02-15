from httplib import BAD_REQUEST
from functools import wraps

from urlobject import URLObject
from flask import render_template, current_app, request, redirect
from flask.ext.restful.reqparse import Argument, RequestParser
from flask.ext.login import LoginManager, AnonymousUser, login_user, user_unauthorized, login_url, make_next_param

from utils.sqlalchemyutils import get_or_create

from .models import User
from .app import app

login_manager = LoginManager()
login_manager.setup_app(app)

class JJAnonymousUser(AnonymousUser):
    def __nonzero__(self):
        return False
    def __repr__(self):
        return '%s()' % (self.__class__.__name__,)
login_manager.anonymous_user = JJAnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_handler():
    user_unauthorized.send(user_unauthorized.send(current_app._get_current_object()))
    url = URLObject(login_url(login_manager.login_view, request.url))
    prev_param = make_next_param(url.without_query(), request.referrer or '/')
    return redirect(url.add_query_param('prev', prev_param).add_query_param('mode', 'action'))

@app.route('/login')
def login():
    return render_template('login.html')

login_manager.login_view = 'login'
login_manager.login_message = None

backends = {}
def backend(*arguments):
    def decor(func):
        @wraps(func)
        def concrete_backend():
            parser = RequestParser()
            for argument in arguments:
                parser.args.append(argument)
            user, created = func(parser.parse_args())
            current_app.db.session.commit()
            login_user(user)
            return user, created
        backends[func.__name__] = concrete_backend
        return concrete_backend
    return decor

class InvalidAuth(Exception):
    def __init__(self, msg, status=BAD_REQUEST):
        self.msg = msg
        self.status = BAD_REQUEST

@backend(Argument('username', required=True))
def demoauth(args):
    user_instance, created = get_or_create(current_app.db, User, username=args['username'])
    return user_instance, created
