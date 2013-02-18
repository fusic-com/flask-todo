from httplib import NO_CONTENT

from flask import request
from flask.ext.restful import fields

from utils.flaskutils.restful import BetterErrorHandlingApi, patched_to_marshallable_type

from .. import models
from ..app import app
from .base import Entity, Collection
from .auth import UserFieldsMixin, Session

# HACK: see https://github.com/twilio/flask-restful/pull/32
fields.to_marshallable_type = patched_to_marshallable_type

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
    def put(self, id):
        todo = models.Todo.query.get_or_404(id)
        todo.title = request.json['title']
        todo.completed = request.json['completed']
        models.db.session.add(todo)
        models.db.session.commit()
        return todo
    def delete(self, id):
        model = self.get(id)
        models.db.session.delete(model)
        models.db.session.commit()
        return '', NO_CONTENT

class Todos(TodoMixin, Collection):
    def post(self):
        todo = models.Todo(title=request.json['title'])
        models.db.session.add(todo)
        models.db.session.commit()
        return todo

api = BetterErrorHandlingApi(app)
api.add_resource(User, '/api/users/<int:id>', endpoint='api_user')
api.add_resource(Users, '/api/users/', endpoint='api_users')
api.add_resource(Todo, '/api/todos/<int:id>', endpoint='api_todo')
api.add_resource(Todos, '/api/todos/', endpoint='api_todos')
api.add_resource(Session, '/api/session', endpoint='api_session')
