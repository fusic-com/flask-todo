from httplib import NO_CONTENT, CONFLICT
from functools import partial

from flask.ext.restful import fields, abort
from flask.ext.restful.reqparse import Argument
from sqlalchemy.exc import IntegrityError

from utils.flaskutils.restful import BetterErrorHandlingApi, patched_to_marshallable_type, parse_with

from .. import models
from ..app import app
from .base import Entity, Collection
from .auth import UserFieldsMixin, Session

# HACK: see https://github.com/twilio/flask-restful/pull/32
fields.to_marshallable_type = patched_to_marshallable_type

JsonArg = partial(Argument, location='json', required=True)

class UserMixin(UserFieldsMixin):
    model = models.User
class User(UserMixin, Entity):
    pass
class Users(UserMixin, Collection):
    pass

class TodoMixin(object):
    model = models.Todo
    fields = {
        'title' : fields.String,
        'completed' : fields.Boolean,
        'id' : fields.Integer
    }
class Todo(TodoMixin, Entity):
    decorator_exemptions = ('DELETE',)
    @parse_with(JsonArg('title'), JsonArg('completed', type=bool))
    def put(self, params, id):
        todo = models.Todo.query.get(id)
        if todo is None:
            todo = models.Todo(id=id)
        for key, value in params.iteritems():
            setattr(todo, key, value)
        models.db.session.add(todo)
        try:
            models.db.session.commit()
        except IntegrityError:
            abort(CONFLICT)
        return todo
    def delete(self, id):
        model = self.get(id)
        models.db.session.delete(model)
        models.db.session.commit()
        return '', NO_CONTENT

class Todos(TodoMixin, Collection):
    @parse_with(JsonArg('title'))
    def post(self, params):
        todo = models.Todo(title=params.title)
        models.db.session.add(todo)
        models.db.session.commit()
        return todo

api = BetterErrorHandlingApi(app)
api.add_resource(User, '/api/users/<int:id>', endpoint='api_user')
api.add_resource(Users, '/api/users/', endpoint='api_users')
api.add_resource(Todo, '/api/todos/<int:id>', endpoint='api_todo')
api.add_resource(Todos, '/api/todos/', endpoint='api_todos')
api.add_resource(Session, '/api/session', endpoint='api_session')
