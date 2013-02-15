#!/usr/bin/env python

from __future__ import print_function

from flask.ext.script import Manager

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
from backend.models import db

manager = Manager(app)

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
