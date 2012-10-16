from flask import (Flask, request, session, g, redirect, url_for,
                   abort, render_template, flash, jsonify)

import hashlib
#import os
#import imp

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
            session['logged_in'] = True
            next = request.form.get('next')
            if next == '':
                next = 'home'
            return redirect(url_for(next))
    
    return render_template('login.html')
    
@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
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
    

    if ('logged_in' not in session and
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

    app.jinja_env.globals['blueprints'] = [
        ('test_route', 'Item 1', 'home'),
        ('test_route', 'Item 2', 'home'),
        ('test_route', 'Item 3', 'home')
    ]