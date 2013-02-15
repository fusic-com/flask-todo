from httplib import OK

from .app import app

@app.route('/')
def index():
    return 'Hello, world!', OK, {"Content-Type": "text/plain"}
