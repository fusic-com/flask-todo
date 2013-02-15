#!/usr/bin/env python

from __future__ import print_function

# import 3rd party libraries
from flask.ext.script import Manager
from werkzeug.serving import run_simple, WSGIRequestHandler

# patch builtins to add INTERACT
import __builtin__
from utils.pyutils import interact
__builtin__.INTERACT = interact

# import settings and initialize app object
from config import settings
from backend.app import initialize_app
app = initialize_app(settings)

# import libraries
from utils.ext.path import Path

# import our code after initialization of app
from config.log import setup_logging
from backend.models import db

manager = Manager(app)
setup_logging('scss')

@manager.command
def runserver(port=5000, bindhost='127.0.0.1'):
    "start the development server"
    class SilentWSGIRequestHandler(WSGIRequestHandler):
        def log_request(self, *args, **kwargs): pass
    run_simple(bindhost, port, app, request_handler=SilentWSGIRequestHandler,
               use_reloader=app.debug, use_debugger=app.debug)

@manager.command
def recreatedb():
    "destroy the database (if any) and recreate it"
    uri = settings.SQLALCHEMY_DATABASE_URI
    if uri.scheme == 'sqlite':
        Path(uri.path).unlink_p()
        pass
    else:
        raise NotImplementedError('unknown database scheme %s' % (uri.scheme,))
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    manager.run()
