import os
import imp

from flask import Flask

BLUEPRINT_DIRECTORY = 'blueprints'

app = Flask(__name__)
app.config.from_object(__name__)

"""
Looks for blueprints, loads them and generates
a blueprints global for jinja
"""

app.jinja_env.globals['blueprints'] = []

path = app.config['BLUEPRINT_DIRECTORY']
dir_list = os.listdir(path)
blueprints = {}

for fname in dir_list:
    if os.path.isdir(os.path.join(path, fname)) and os.path.exists(os.path.join(path, fname, '__init__.py')):
        f, filename, descr = imp.find_module(fname, [path])
        blueprints[fname] = imp.load_module(fname, f, filename, descr)
        
    elif os.path.isfile(os.path.join(path, fname)):
        name, ext = os.path.splitext(fname)
        if ext == '.py' and not name == '__init__':
            f, filename, descr = imp.find_module(name, [path])
            blueprints[fname] = imp.load_module(name, f, filename, descr)

for blueprint in blueprints.values():
    
    blueprint_name = getattr(blueprint, '__name__')
    blueprint = getattr(blueprint, blueprint_name, blueprint)
    
    blueprint_label = getattr(blueprint, 'LABEL', None)
    blueprint_icon = getattr(blueprint, 'ICON', 'link')
            
    app.register_blueprint(getattr(blueprint, 'blueprint'), url_prefix='/%s' % blueprint_name)
    if blueprint_label:
        app.jinja_env.globals['blueprints'].append( ("%s.index"%blueprint_name, blueprint_label, blueprint_icon) )
    
app.config['registered_blueprints'] = blueprints
