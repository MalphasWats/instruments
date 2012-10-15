from flask import (Flask, request, session, g, redirect, url_for,
                   abort, render_template, flash, jsonify)

#import os
#import imp

#from functools import wraps

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    return render_template('layout.html')