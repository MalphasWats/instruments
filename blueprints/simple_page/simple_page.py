from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

module = Blueprint('simple_page', __name__,
                        template_folder='templates')
                        
                        
LABEL = 'Simple Page'
PUBLIC_ENDPOINTS = ['index']


@module.route('/page/')
def index():
    try:
        return render_template('simple_page.html')
    except TemplateNotFound:
        abort(404)