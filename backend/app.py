from logging import getLogger
from os import environ

from flask import Flask, send_from_directory
from sqlalchemy import event
from sqlalchemy.engine import Engine

from utils.flaskutils import install_request_logger
from utils.ext.path import Path

app = None

def initialize_logging(settings):
    # UGLY: I don't know how to count CPU time accurately in a multithreaded environment and I'm too lazy
    #       to implement proper query counting for a multithreaded environment. Not sure how to test this
    #       reliably, I resort to checking if we run under the Werkzeug reloader as a means to decide whether or
    #       not to count CPU time and database queries when logging. Rough, but effective.
    count_cpu_usage_and_db_queries = 'WERKZEUG_RUN_MAIN' in environ
    logging_exemptions = () if 'JJ_DEBUG_ASSETS' in environ else ('/static/', '/system/admin/static/', '/system/rq/')
    query_count_increment = install_request_logger(app, count_cpu_usage_and_db_queries, getLogger('jj.request'),
                                                   logging_exemptions)
    if count_cpu_usage_and_db_queries:
        event.listens_for(Engine, "after_cursor_execute")(query_count_increment)

def initialize_app(settings):
    global app
    app = Flask(__name__)
    app.config.from_object(settings)

    # ORDER MIGHT BE IMPORTANT BELOW THIS LINE
    # install extensions and import modules that do registrations
    # the `import x; x` idiom silences pyflakes etc

    import models ; models # must import models before we can init logging, so logging can count queries
    initialize_logging(settings)
    import views ; views
    import assets ; assets
    import api ; api
    import auth ; auth

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(Path(app.root_path)/'static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    return app
