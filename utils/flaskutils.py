import os
import json

from flask import current_app
from webassets.filter import Filter

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
