from flask import (Flask, request, session, g, redirect, url_for,
                   abort, render_template, flash, jsonify)

import hashlib
import os
import imp

import database

#from functools import wraps

SECRET_KEY = 'banana'
#PUBLIC_ENDPOINTS = ['login', 'static', 'test_route']

app = Flask(__name__)
app.config.from_object(__name__)


def public_endpoint(function):
    function.is_public = True
    return function
    
    
@app.before_request
def check_valid_login():
    # if request.endpoint is in list of things that don't need a login (??!?), carry on
    # if no session at all, throw back to login
    # check session hash against the database, make sure it's still valid
    # if not valid, throw back to login
    login_valid = 'user' in session
    
    
    if (request.endpoint and 
        'static' not in request.endpoint and 
        not login_valid and 
        not getattr(app.view_functions[request.endpoint], 'is_public', False) ) :
        return render_template('login.html', next=request.endpoint)
    

@app.route('/')
def home():
    return render_template('layout.html')
    
    
@app.route('/login/', methods=['POST', 'GET'])
@public_endpoint
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password_plaintext = request.form.get('password')
        if username != '' and password_plaintext != '':
            user = database.check_login_details(username, password_plaintext)
            if user:
                # generate a session hash
                # store the session hash in the database & session cookie
                session['user'] = dict(user)
                next = request.form.get('next')
                if next == '' or next == 'login':
                    next = 'home'
                return redirect(url_for(next))
            else:
                flash("incorrect username/password.", category='error')
    
    return render_template('login.html')
    
    
@app.route('/logout/')
@public_endpoint
def logout():
    session.pop('user', None)
    print session
    return redirect(url_for('home'))
    
    
@app.route('/admin/')
def admin():
    blueprints = []
    for blueprint in app.config['registered_blueprints'].values():
        blueprint_name = getattr(blueprint, '__name__')
        blueprint = getattr(blueprint, blueprint_name, blueprint)
        
        blueprint_description = getattr(blueprint, '__doc__', None) or ''
        blueprint_label = getattr(blueprint, 'LABEL', blueprint_name)
        
        if hasattr(blueprint, 'get_admin_panel'):
            panel_content = blueprint.get_admin_panel()
        else:
            panel_content = ''
        
        blueprints.append( {'name': blueprint_name, 'label': blueprint_label, 'description': blueprint_description, 'content': panel_content} )
    return render_template('admin.html', registered_blueprints=blueprints)


@app.route('/test/')
@public_endpoint
def test_route():
    #app.config['PUBLIC_ENDPOINTS'].append('admin')
    print "test reached"
    return render_template('admin.html')
    #return redirect(url_for('home'))
    
    
def is_public_endpoint(endpoint):
    return endpoint in app.config['PUBLIC_ENDPOINTS']
    
    
def load_blueprints():
    """ 
    Called in __init__.py on first startup. 

    Looks for blueprints, loads them and generates
    a blueprints global for jinja
    """
    
    app.jinja_env.globals['blueprints'] = []
    
    path = 'blueprints'
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
        
        blueprint_label = getattr(blueprint, 'LABEL', blueprint_name)
        blueprint_icon = getattr(blueprint, 'ICON', 'link')
            
        # if hasattr(blueprints[fname], 'PUBLIC_ENDPOINTS'):
            # app.config['PUBLIC_ENDPOINTS'] = app.config['PUBLIC_ENDPOINTS'] + getattr(blueprints[fname], 'PUBLIC_ENDPOINTS')
                
        app.register_blueprint(getattr(blueprint, 'module'), url_prefix='/%s' % blueprint_name)
        app.jinja_env.globals['blueprints'].append( ("%s.index"%blueprint_name, blueprint_label, blueprint_icon) )
        
    app.config['registered_blueprints'] = blueprints