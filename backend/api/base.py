from httplib import NO_CONTENT
from functools import wraps

from flask import request
from flask.ext.restful import marshal, marshal_with, Resource
from flask.ext.restful.reqparse import Argument

from utils.datautils import positive_integer
from utils.flaskutils import CustomHTTPException
from utils.flaskutils.restful import parse_with

class lazy_marshal_with(marshal_with):
    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            fields = self.fields() if callable(self.fields) else self.fields
            return marshal(f(*args, **kwargs), fields)
        return wrapper

class Marshallable(Resource):
    decorator_exemptions = ()
    @property
    def method_decorators(self):
        if request.method in self.decorator_exemptions:
            return ()
        if not hasattr(self, 'fields'):
            return ()
        return (lazy_marshal_with(self.fields),)

class Entity(Marshallable):
    def build_query(self):
        return self.model.query
    def get(self, id):
        return self.build_query().get_or_404(id)
class Collection(Marshallable):
    PAGINATION_PARAMETER = 'page'
    ITEMS_PARAMETER = 'items'
    ITEMS_MAXIMUM = ITEMS_DEFAULT = 50
    ORDER_ATTRIBUTE = 'id'
    def build_query(self):
        return self.model.query.order_by(getattr(self.model, self.ORDER_ATTRIBUTE))
    @parse_with(
        Argument(PAGINATION_PARAMETER, type=positive_integer, help="page must be a positive integer"),
        Argument(ITEMS_PARAMETER, type=positive_integer, help="items must be a positive integer"),
    )
    def paginate(self, params, query):
        paginated = query.paginate(
            params[self.PAGINATION_PARAMETER] or 1,
            min(params[self.ITEMS_PARAMETER] or self.ITEMS_DEFAULT, self.ITEMS_MAXIMUM),
            error_out=False
        )
        if params[self.PAGINATION_PARAMETER] and paginated.pages < params.page:
            raise CustomHTTPException(code=NO_CONTENT)
        return paginated.items
    @parse_with(Argument('feeder', type=int))
    def get(self, params):
        if params.feeder:
            return self.build_query().all()
        return self.paginate(self.build_query())
