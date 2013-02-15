from functools import wraps

from flask import request

from flask.ext.restful import Api
from flask.ext.restful.reqparse import RequestParser

def patched_to_marshallable_type(obj):
    """adds __marshallable__ support; see https://github.com/twilio/flask-restful/pull/32"""
    if obj is None:
        return None  # make it idempotent for None

    if hasattr(obj, '__getitem__'):
        return obj  # it is indexable it is ok

    if hasattr(obj, '__marshallable__'):
        return obj.__marshallable__()

    return dict(obj.__dict__)

class BetterErrorHandlingApi(Api):
    # HACK: see https://github.com/twilio/flask-restful/issues/8
    #       and https://github.com/twilio/flask-restful/pull/29
    def __init__(self, app, prefix='', default_mediatype='application/json',
                 decorators=None):
        self.saved_handle_exception = app.handle_exception
        self.saved_handle_user_exception = app.handle_user_exception
        super(BetterErrorHandlingApi, self).__init__(app, prefix, default_mediatype, decorators)
        app.handle_exception = self.handle_exception
        app.handle_user_exception = self.handle_user_exception
        self.endpoints = set()
    def add_resource(self, resource, *urls, **kwargs):
        endpoint = kwargs.setdefault('endpoint', resource.__name__.lower())
        self.endpoints.add(endpoint)
        return super(BetterErrorHandlingApi, self).add_resource(resource, *urls, **kwargs)
    def handle_exception(self, e):
        return self.handle_error(self.saved_handle_exception, e)
    def handle_user_exception(self, e):
        return self.handle_error(self.saved_handle_user_exception, e)
    def handle_error(self, original, e):
        rv = original(e) # call original error handler, so any side-effect causing handling (sentry, etc) will happen
        if not request.url_rule or request.url_rule.endpoint not in self.endpoints:
            return rv
        return super(BetterErrorHandlingApi, self).handle_error(e)

def parse_with(*arguments, **kwargs):
    """This decorator allows you to easily augment any method (typically a
       view method) to access reqparse based arguments, i.e.:

       class Users(Resource):
           @parse_with(Argument('profession'))
           def post(self, params, username):
               create_new_user(username, params.profession)
               return 'CREATED', 201

       api.add_resource(Users, '/<username>', endpoint='users')
    """
    parser = kwargs.pop('parser', RequestParser())
    if kwargs: # mimic py3k style named-arguments after *args, i.e., def f(a, *b, c=1)
        raise TypeError("unexpected keyword argument '%s'" % (kwargs.popitem()[0],))
    for argument in arguments:
        parser.args.append(argument)
    def decor(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            return func(self, parser.parse_args(), *args, **kwargs)
        return inner
    return decor
