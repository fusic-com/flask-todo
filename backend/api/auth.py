from httplib import NO_CONTENT, OK, CREATED, RESET_CONTENT

from flask.ext.restful import Resource, fields, marshal
from flask.ext.restful.reqparse import Argument
from flask.ext.login import current_user, logout_user

from utils.flaskutils.restful import parse_with

from ..auth import backends, InvalidAuth
class UserFieldsMixin(object):
    fields = {"username": fields.String}

class Session(UserFieldsMixin, Resource):
    def marshal(self, user):
        try:
            user = user._get_current_object() # marshal() has issues with serializing flask's proxied objects
        except AttributeError:
            pass
        return marshal(user, self.fields() if callable(self.fields) else self.fields)
    def get(self):
        if current_user:
            return self.marshal(current_user), OK
        return None, NO_CONTENT
    def delete(self):
        if not current_user:
            return None, NO_CONTENT
        logout_user()
        return None, RESET_CONTENT
    @parse_with(Argument('kind', required=True, choices=backends))
    def put(self, params):
        try:
            user, created = backends[params.kind]()
            return self.marshal(user), CREATED if created else OK
        except InvalidAuth, error:
            return {"message": error.msg}, error.status
