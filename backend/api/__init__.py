from flask.ext.restful import fields

from utils.flaskutils.restful import BetterErrorHandlingApi, patched_to_marshallable_type

from .. import models
from ..app import app
from .base import Entity, Collection

# HACK: see https://github.com/twilio/flask-restful/pull/32
fields.to_marshallable_type = patched_to_marshallable_type

class UserMixin(object):
    fields = {"username": fields.String}
    model = models.User
class User(UserMixin, Entity):
    pass
class Users(UserMixin, Collection):
    pass

api = BetterErrorHandlingApi(app)
api.add_resource(User, '/api/users/<int:id>', endpoint='api_user')
api.add_resource(Users, '/api/users/', endpoint='api_users')
