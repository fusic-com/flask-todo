from flask.ext.restful import Api

from .app import app

api = Api(app)
