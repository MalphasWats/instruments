from flask import (Flask, request, session, g, redirect, url_for,
                   abort, render_template, flash, jsonify)

import hashlib
import os
import imp

#from functools import wraps

SECRET_KEY = 'banana'
PUBLIC_ENDPOINTS = ['login', 'static', 'test_route']

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    return render_template('layout.html')
    
    
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password_plaintext = request.form.get('password')
        if username != '' and password_plaintext != '':
            password_hash = hashlib.sha512(password_plaintext).hexdigest()
            # check details are correct
            # generate a session hash
            # store the session hash in the database & session cookie
            session['user'] = {'forename': 'Michael', 'surname': 'Watts'}
            next = request.form.get('next')
            if next == '' or next == 'login':
                next = 'home'
            return redirect(url_for(next))
    
    return render_template('login.html')
    
@app.route('/logout/')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))
    
    
@app.route('/admin/')
def admin():
    return render_template('admin.html')
    
    
@app.before_request
def check_login():
    # if request.endpoint is in list of things that don't need a login (??!?), carry on
    # if no session at all, throw back to login
    # check session hash against the database, make sure it's still valid
    # if not valid, throw back to login
    

    if ('user' not in session and
        not is_public_endpoint(request.endpoint)):
        return render_template('login.html', next=request.endpoint)
    

@app.route('/test/')
def test_route():
    app.config['PUBLIC_ENDPOINTS'].append('admin')
    return redirect(url_for('home'))
    
    
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
            
            blueprint_name = getattr(blueprints[fname], '__name__')
            if hasattr(blueprints[fname], 'LABEL'):
                blueprint_label = getattr(blueprints[fname], 'LABEL')
            else:
                blueprint_label = blueprint_name
                
            if hasattr(blueprints[fname], 'ICON'):
                blueprint_icon = getattr(blueprints[fname], 'ICON')
            else:
                blueprint_icon = 'link'
                
            if hasattr(blueprints[fname], 'PUBLIC_ENDPOINTS'):
                app.config['PUBLIC_ENDPOINTS'] = app.config['PUBLIC_ENDPOINTS'] + getattr(blueprints[fname], 'PUBLIC_ENDPOINTS')
            
            app.register_blueprint(getattr(blueprints[fname], 'module'), url_prefix='/%s' % blueprint_name)
            app.jinja_env.globals['blueprints'].append( ("%s.index"%blueprint_name, blueprint_label, blueprint_icon) )
            
        # elif os.path.isfile(os.path.join(path, fname)):
            # name, ext = os.path.splitext(fname)
            # if ext == '.py' and not name == '__init__':
                # f, filename, descr = imp.find_module(name, [path])
                # mods[fname] = imp.load_module(name, f, filename, descr)
                # app.register_blueprint(getattr(mods[fname], 'module'))

    # app.jinja_env.globals['blueprints'] = [
        # ('test_route', 'Item 1', 'home'),
        # ('test_route', 'Item 2', 'home'),
        # ('test_route', 'Item 3', 'home')
    # ]