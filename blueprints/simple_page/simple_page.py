""" A Simple Page Blueprint """
from flask import Blueprint, render_template, abort, redirect, request
from jinja2 import TemplateNotFound

from instruments.core import public_endpoint

blueprint = Blueprint('simple_page', __name__,
                        template_folder='templates')
                        
                        
LABEL = 'Simple Page'
ADMIN_LABEL = 'Simple Page Administration'
ICON = 'globe'


@blueprint.route('/page/')
@public_endpoint
def index():
    try:
        return render_template('simple_page.html')
    except TemplateNotFound:
        abort(404)
        
        
@blueprint.route('/test/', methods=['POST'])
def test():
    return redirect("%s#%s" % (request.referrer, blueprint.name))
        
        
def get_admin_panel():
    return render_template('widgets/admin_panel.html')