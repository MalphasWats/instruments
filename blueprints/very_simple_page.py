"""A very simple page"""

from flask import Blueprint

LABEL = "Very Simple Page"

blueprint = Blueprint('very_simple_page', __name__,
                        template_folder='templates')


@blueprint.route('/very_simple_page')
def index():
    return """<html>
    <head>
    <title>Very Simple Page</title>
    </head>
    <body>
    <h1>Very Simple Page</h1>
    <p>This is a very simple Page</p>
    </body>
    </html>"""
    