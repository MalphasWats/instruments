"""A very simple page"""

from flask import Blueprint, render_template

LABEL = "Very Simple Page"

blueprint = Blueprint('very_simple_page', __name__,
                        template_folder='templates')


@blueprint.route('/very_simple_page')
def index():
    return render_template('page.html', page_title="Very Simple Page", page_content="<p>Very Simple Page</p>")
    