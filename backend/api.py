from flask.ext.restful import fields

from utils.flaskutils.restful import BetterErrorHandlingApi, patched_to_marshallable_type

from .app import app

# HACK: see https://github.com/twilio/flask-restful/pull/32
fields.to_marshallable_type = patched_to_marshallable_type

api = BetterErrorHandlingApi(app)
