#!/usr/bin/env python

from __future__ import print_function

from flask.ext.script import Manager

# import settings and initialize app object
from config import settings
from backend.app import initialize_app
app = initialize_app(settings)

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
