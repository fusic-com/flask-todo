from os import path
from glob import glob
from functools import partial
from collections import defaultdict

from flask.ext.assets import Environment, Bundle
from webassets.filter import register_filter, get_filter

from config.cdn import proxied

from utils.flaskutils import RegisterJst
from utils.ext.bunch import Bunch
from utils.ext.path import Path

from .app import app

Coffee = partial(Bundle, filters='coffeescript', debug=False)
SCSS = partial(Bundle, filters='pyscss', debug=False)
JS = partial(Bundle, filters='yui_js')
CSS = partial(Bundle, filters='yui_css')

assets = Environment(app)
assets.url = proxied('/static/')

class Special(str): pass
class Depends(Special): pass

asset_spec = {
    "index.js": ('index/*.coffee','index/*.jst',),
    "index.css": ('index/*.scss',),
    "todo.js": ('todo/jst/*.jst',),
}

def get_rules(kind):
    if kind == '.css':
        return Bunch(
            final_filter = ["yui_css", get_filter('cssrewrite', replace=proxied)],
            compilers = {".scss": "pyscss"},
            kwargs = defaultdict(dict)
        )
    elif kind == '.js':
        return Bunch(final_filter="yui_js", compilers={".coffee": "coffeescript", ".jst": "register_jst"},
                     kwargs=defaultdict(dict))
    raise RuntimeError("unknown bundle kind: %s" % (kind,))
def yield_expanded(iterable):
    already_yielded = set()
    base = Path(app.static_folder)
    for element in iterable:
        if isinstance(element, Special):
            yield element
            continue
        for atom in sorted(base.relpathto(expanded) for expanded in glob(base/element)):
            if atom in already_yielded:
                continue
            already_yielded.add(atom)
            yield atom
def register_assets(spec):
    for name, elements in spec.iteritems():
        name, kind = path.splitext(name)
        rules = get_rules(kind)
        filemap = defaultdict(list)
        for element in yield_expanded(elements):
            _, extension = path.splitext(element)
            if isinstance(element, Depends):
                rules.kwargs[extension]['depends'] = element
                continue
            filemap[extension].append(element)

        contents = list(filemap.get(kind, []))
        for compiled_extension, compiled_filters in rules['compilers'].iteritems():
            if compiled_extension in filemap:
                kwargs = rules.kwargs.get(compiled_extension, {})
                contents.append(Bundle(*filemap[compiled_extension], filters=compiled_filters, debug=False,
                                output="gen/%s.%%(version)s%s%s" % (name, compiled_extension, kind), **kwargs))
        assets.register(
            name + kind,
            Bundle(*contents, filters=rules.final_filter, output="gen/%s.%%(version)s%s" % (name, kind),
                   **rules.kwargs[kind])
        )
register_filter(RegisterJst)
register_assets(asset_spec)

