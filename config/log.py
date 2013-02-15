import logging

from flask import g
from clint.textui import colored

from utils.datautils import thresholds

def context_id():
    return 'rqid', g.uuid.hex

class ColoredStreamHandler(logging.StreamHandler):
    def format(self, record):
        s = super(ColoredStreamHandler, self).format(record)
        return thresholds(record.levelno, (
            (colored.green, logging.INFO),
            (colored.blue, logging.WARNING),
            (colored.yellow, logging.ERROR),
            (colored.red, logging.CRITICAL)
        ), colored.magenta)(s)

class ContextFilter(logging.Filter):
    def filter(self, record):
        try:
            namespace, id = context_id()
            record.context_id = ':'.join((namespace, id[:6]))
        except RuntimeError:
            record.context_id = '<nocontext>'
        return True

def setup_logging(*roots, **kwargs):
    if hasattr(setup_logging, 'done'):
        return
    setup_logging.done = True
    level = kwargs.pop('level', logging.DEBUG)
    formatter = logging.Formatter('[%(process)05d/%(threadName)-10s] [%(levelno)02d] %(context_id)s '
                                  '%(name)-12s %(message)s')
    handler = ColoredStreamHandler()
    handler.setFormatter(formatter)
    handler.addFilter(ContextFilter())
    for root_name in {'jj'}.union(roots):
        logger = logging.getLogger(root_name)
        logger.addHandler(handler)
        logger.setLevel(level)
