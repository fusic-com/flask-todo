from os import environ

from utils.ext.path import Path
try:
    from urlobject import URLObject as Url
except ImportError:
    if 'JJ_VALIDATE_CONFIG' not in environ:
        raise
    class Url(object):
        __init__ = lambda s, *a: None
        __getattr__ = __call__ = lambda s, *a: s

required = lambda s: environ[s]
optional = lambda s, d=None: environ.get(s, d)
boolean = lambda v: bool(int(v))
netloc = lambda n: Url().with_netloc(n)

try:
    DEBUG=boolean(required('DEBUG'))
    VAR_DIR=Path(required('VAR_DIR'))
    SERVER_NAME=required("SERVER_NAME")
    SERVER_URL=netloc(SERVER_NAME)
    AWS_ACCESS_KEY_ID=optional('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY=optional('AWS_SECRET_ACCESS_KEY')
    SQLALCHEMY_DATABASE_URI = Url(required('DATABASE_URL'))
    SECRET_KEY=required('SECRET_KEY')
except KeyError, key:
    raise SystemExit("environment missing required key %s" % (key,))

del required, optional, boolean
