from os import environ

from utils.ext.path import Path
from urlobject import URLObject as Url

required = lambda s: environ[s]
optional = lambda s, d=None: environ.get(s, d)
boolean = lambda v: bool(int(v))
netloc = lambda n: Url().with_netloc(n)

DEBUG=boolean(required('DEBUG'))
VAR_DIR=Path(required('VAR_DIR'))
SERVER_NAME=required("SERVER_NAME")
SERVER_URL=netloc(SERVER_NAME)
AWS_ACCESS_KEY_ID=optional('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=optional('AWS_SECRET_ACCESS_KEY')
SQLALCHEMY_DATABASE_URI = Url(required('DATABASE_URL'))

del required, optional, boolean
