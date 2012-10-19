""" A Simple Page Blueprint """
from flask import Blueprint, render_template, abort, redirect, request
from jinja2 import TemplateNotFound

from instruments.core import public_endpoint

module = Blueprint('simple_page', __name__,
                        template_folder='templates')
                        
                        
LABEL = 'Simple Page'
ADMIN_LABEL = 'Simple Page Administration'
ICON = 'globe'


@module.route('/page/')
@public_endpoint
def index():
    try:
        return render_template('simple_page.html')
    except TemplateNotFound:
        abort(404)
        
        
@module.route('/test/', methods=['POST'])
def test():
    return redirect("%s#%s" % (request.referrer, module.name))
        
        
def get_admin_panel():
    return render_template('admin/admin_panel.html')