from httplib import INTERNAL_SERVER_ERROR
from uuid import uuid4
import json
import logging
import os

from flask import current_app, request, g, session
from werkzeug.exceptions import HTTPException
from webassets.filter import Filter

from ..datautils import CPUTime, Timer, thresholds

class RegisterJst(Filter):
    name = "register_jst"
    def input(self, _in, out, source_path, **kwargs):
        template_data = _in.read()
        assert source_path.find(current_app.static_folder) == 0
        source_path = source_path[len(current_app.static_folder):].lstrip(os.path.sep)
        wrapped_template = "register_template(%s, %s);" %(json.dumps(source_path), json.dumps(template_data))
        out.write(wrapped_template)

    def output(self, _in, out, **kwargs):
        out_data = _in.read()
        out_data = """(function(){
        window.jj = window.jj || {};
        window.jj.jst = window.jj.jst || {};
        var register_template = function(name, data){
            window.jj.jst[name] = data;
        };
        %s
        })();""" %(out_data,)
        out.write(out_data)

class CustomHTTPException(HTTPException):
    def __init__(self, body=None, code=INTERNAL_SERVER_ERROR, headers=None):
        self.body = '' if body is None else body
        self.code = code
        self.headers = headers or {}
    def get_body(self, environ):
        return self.body

def install_request_logger(app, single_threaded, logger, *unlogged_prefixes):
    def make_context(**kwargs):
        location = request.path
        if request.query_string:
            location += "?" + request.query_string
        return dict(
            uuid = g.uuid,
            method = request.method[:4],
            location = location,
            **kwargs
        )
    def should_skip_logging():
        for prefix in unlogged_prefixes:
            if request.path.startswith(prefix):
                return True
        return False
    @app.before_request
    def logging_before():
        g.uuid = uuid4()
        g.timer = Timer()
        g.cpu = CPUTime()
        g.queries = 0
        if should_skip_logging():
            return
        try:
            size = int(request.headers['Content-Length'])
        except (KeyError, ValueError):
            size = -1
        try:
            g.userid = int(session['user_id'])
        except (KeyError, ValueError):
            g.userid = -1
        logger.debug('>     %(method)-4s %(location)s agent=%(agent)s userid=%(userid)d size=%(size)d', make_context(
            agent=request.user_agent.browser, userid=g.userid, size=size,
        ))
    @app.after_request
    def logging_after(response):
        if should_skip_logging():
            return response
        level = thresholds(response.status_code, (
            (logging.DEBUG, 300),
            (logging.INFO, 400),
            (logging.WARNING, 500),
            (logging.ERROR, 600)
        ), logging.CRITICAL)
        try:
            size = int(response.headers['Content-Length'])
        except (KeyError, ValueError):
            size = -1
        context = make_context(
            status=response.status_code, wall=g.timer.elapsed, response_size=size, secure=request.is_secure,
            agent=request.user_agent.string, ip=request.access_route[0], rqid=g.uuid.hex[:6], userid=g.userid
        )
        fmt = '< %(status)d %(method)-4s %(location)s wall=%(wall).1f size=%(response_size)d'
        if single_threaded:
            context.update(queries=g.queries, cpu=round(g.cpu.elapsed, 3))
            fmt += ' cpu=%(cpu).1f queries=%(queries)d'
        logger.log(level, fmt, context)
        return response
    def query_count_increment(*a):
        g.queries += 1
    return query_count_increment
